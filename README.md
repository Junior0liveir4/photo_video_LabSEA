
# 📷🎥 photo_video_LabSEA

Este projeto tem como objetivo exibir uma **transmissão de vídeo em tempo real** recebida via **mensageria AMQP**, permitindo ao usuário **salvar imagens** ou **gravar vídeos** com comandos simples de teclado. É uma ferramenta útil para visualização, coleta e registro de dados visuais em ambientes laboratoriais como o **LabSEA**.

---

## 📌 Funcionalidades

- 🔁 Exibe vídeo em tempo real proveniente de um tópico AMQP.
- 📸 Permite salvar o frame atual como imagem pressionando a tecla **`s`**.
- 🎞️ Permite iniciar/parar gravação de vídeo pressionando a tecla **`r`**.
- 💾 Os arquivos são salvos automaticamente em um diretório especificado.
- ❌ Encerramento seguro do sistema ao pressionar **`q`**.

---

## 🧰 Requisitos

### 📦 Bibliotecas Python

Este projeto requer Python 3 e as seguintes bibliotecas:

```bash
pip install numpy opencv-python is-wire
```

> Certifique-se de que o pacote `is-wire` está instalado corretamente, pois ele permite o consumo de mensagens AMQP e é utilizado para receber os frames da câmera.

---

## 📂 Estrutura de diretórios

```
photo_video_LabSEA/
├── photo_video_LabSEA.py     # Código principal
├── README.md                 # Este arquivo
└── output_media/             # (Criado automaticamente) Diretório onde imagens e vídeos são salvos
```

---

## ⚙️ Configurações importantes

Dentro do código, há algumas variáveis que podem ser personalizadas:

```python
camera_id = 4  # ID da câmera que está transmitindo no tópico AMQP
broker_uri = "amqp://rabbitmq:30000"  # URI do servidor de mensagens
output_directory = "./output_media"  # Caminho onde vídeos e imagens serão salvos
output_video_name = os.path.join(output_directory, 'output_video.avi')  # Nome do arquivo de vídeo
fps = 20  # Taxa de quadros do vídeo
```

---

## 🚀 Como usar

1. **Clone o repositório (ou copie o código):**
   ```bash
   git clone https://github.com/seu-usuario/photo_video_LabSEA.git
   cd photo_video_LabSEA
   ```

2. **Execute o script principal:**
   ```bash
   python photo_video_LabSEA.py
   ```

3. **Durante a execução:**
   - Pressione **`s`** para salvar o frame atual como uma imagem (`frame_X.jpg`);
   - Pressione **`r`** para iniciar/parar a gravação de vídeo (`output_video.avi`);
   - Pressione **`q`** para encerrar o programa com segurança.

---

## 📦 Salvamento dos arquivos

- Os arquivos são salvos no diretório `output_media/`, que será criado automaticamente se não existir.
- O nome dos arquivos de imagem segue o padrão: `frame_1.jpg`, `frame_2.jpg`, ...
- O vídeo é salvo como `output_video.avi`. Ele será sobrescrito se uma nova gravação for iniciada.

---

## 👨‍🔬 Aplicação

Este código foi desenvolvido no contexto do **LabSEA**, com o objetivo de auxiliar em experimentos visuais, captura de dados de câmeras e análise posterior.

---

## 📃 Licença

Este projeto pode ser utilizado livremente para fins acadêmicos e educacionais. Para outros usos, consulte a equipe responsável pelo LabSEA.

---
