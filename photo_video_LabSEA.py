from is_wire.core import Channel, Subscription
from is_msgs.image_pb2 import Image
import numpy as np
import cv2
import socket
import os

# Classe personalizada para canal de streaming
class StreamChannel(Channel):
    def __init__(self, uri="amqp://guest:guest@10.10.2.211:30000", exchange="is"):
        super().__init__(uri=uri, exchange=exchange)

    def consume_last(self, return_dropped=False):
        dropped = 0
        try:
            msg = super().consume(timeout=0.1)
        except socket.timeout:
            return False

        while True:
            try:
                msg = super().consume(timeout=0.0)
                dropped += 1
            except socket.timeout:
                return (msg, dropped) if return_dropped else msg

# Converte imagem protobuf para numpy
def to_np(input_image):
    if isinstance(input_image, np.ndarray):
        return input_image
    elif isinstance(input_image, Image):
        buffer = np.frombuffer(input_image.data, dtype=np.uint8)
        return cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
    return np.array([], dtype=np.uint8)

# Função para salvar imagem apertando 's'
def save_frame_image(frame, index, output_dir):
    filename = os.path.join(output_dir, f"frame_{index}.jpg")
    cv2.imwrite(filename, frame)
    print(f"[INFO] Frame salvo como {filename}")

# Função para gravar vídeo até o usuário apertar 'r' novamente
def record_video(output_path, frame_size, fps, channel, subscription):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
    print(f"[INFO] Iniciando gravação em '{output_path}' (pressione 'r' para parar)")

    while True:
        msg = channel.consume_last()
        if type(msg) != bool:
            img = msg.unpack(Image)
            frame = to_np(img)
            video_writer.write(frame)
            cv2.imshow("Stream", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('r'):
                print(f"[INFO] Gravação encerrada e salva como '{output_path}'")
                break
            elif key == ord('q'):
                print("[INFO] Encerrando...")
                video_writer.release()
                cv2.destroyAllWindows()
                exit()

    video_writer.release()

# Configurações
camera_id = 4
broker_uri = "amqp://guest:guest@10.10.2.211:30000"
output_directory = "/homes/joliveira/Desktop/Junior/Fotos_Vídeos"
output_video_name = os.path.join(output_directory, 'output_video.avi')
fps = 20

# Garante que o diretório de saída exista
os.makedirs(output_directory, exist_ok=True)

# Inicializações
#topic = 'UndistortedCamera.{}.Frame'
topic = 'CameraGateway.{}.Frame'
channel = StreamChannel(broker_uri)
subscription = Subscription(channel=channel)
subscription.subscribe(topic=topic.format(camera_id))

frame_index = 1
frame_size = None

# Loop principal de exibição
while True:
    msg = channel.consume_last()
    if type(msg) != bool:
        img = msg.unpack(Image)
        frame = to_np(img)

        if frame_size is None:
            frame_size = (frame.shape[1], frame.shape[0])  # (width, height)

        cv2.imshow("Stream", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            save_frame_image(frame.copy(), frame_index, output_directory)
            frame_index += 1

        elif key == ord('r'):
            record_video(output_video_name, frame_size, fps, channel, subscription)

        elif key == ord('q'):
            print("[INFO] Encerrando...")
            break

# Cleanup
cv2.destroyAllWindows()