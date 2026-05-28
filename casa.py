import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

Window = None
Shader_programm = None
Vao_casa = None
Vao_arvore = None
Vao_estrela = None
WIDTH = 800
HEIGHT = 600

def redimensionaCallback(window, w, h):
    global WIDTH, HEIGHT
    WIDTH = w
    HEIGHT = h

def inicializaOpenGL():
    global Window, WIDTH, HEIGHT

    #Inicializa GLFW
    glfw.init()

    #Criação de uma janela
    Window = glfw.create_window(WIDTH, HEIGHT, "Exemplo - renderização de um triângulo", None, None)
    if not Window:
        glfw.terminate()
        exit()

    glfw.set_window_size_callback(Window, redimensionaCallback)
    glfw.make_context_current(Window)

    print("Placa de vídeo: ",OpenGL.GL.glGetString(OpenGL.GL.GL_RENDERER))
    print("Versão do OpenGL: ",OpenGL.GL.glGetString(OpenGL.GL.GL_VERSION))

def inicializaCasa():
    global Vao_casa

    # VAO da casa
    Vao_casa = glGenVertexArrays(1)
    glBindVertexArray(Vao_casa)

    # VBO dos vértices
    points = [
		 # triângulo 1
		0.5, 0.5, 0.0, #vertice superior direito
		0.5, -0.5, 0.0, #vertice inferior direito
		-0.5, -0.5, 0.0, #vertice inferior esquerdo
		#triângulo 2
		-0.5, 0.5, 0.0, #vertice superior esquerdo
		0.5, 0.5, 0.0, #vertice superior direito
		-0.5, -0.5, 0.0, #vertice inferior esquerdo
		#triângulo 3
		0.75, 0.5, 0.0, #vertice superior direito
		-0.75, 0.5, 0.0, #vertice superior esquerdo
		0.0, 1.0, 0.0,  #telhado
        #triângulo 4
        -0.15,-0.5, 0.0, #vertice inferior esquerdo da porta
        0.15, -0.5, 0.0, #vertice inferior direito da porta
        0.15, 0.0, 0.0, #vertice superior direito da porta
        #triângulo 5
        -0.15,0.0, 0.0, #vertice superior esquerdo da porta
        -0.15,-0.5, 0.0, #vertice inferior esquerdo da porta
        0.15, 0.0, 0.0 #vertice superior direito da porta
	]

    points = np.array(points, dtype=np.float32)

    pvbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, pvbo)
    glBufferData(GL_ARRAY_BUFFER, points, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)


    # VBO das cores
    cores = [
		#triângulo 1
		0.0, 1.0, 1.0,#ciano
		0.0, 1.0, 1.0,#ciano
		0.0, 1.0, 1.0,#ciano
		#triângulo 2
		0.0, 1.0, 1.0,#ciano
		0.0, 1.0, 1.0,
		0.0, 1.0, 1.0,#ciano
        #triângulo 3
        1.0, 0.0, 0.0,#vermelho
        1.0, 0.0, 0.0,#vermelho
        1.0, 0.0, 0.0,#vermelho
        #triângulo 4
        0.6, 0.3, 0.0,#marrom
        0.6, 0.3, 0.0,#marrom
        0.6, 0.3, 0.0,#marrom
        #triângulo 5
        0.6, 0.3, 0.0,#marrom
        0.6, 0.3, 0.0,#marrom
        0.6, 0.3, 0.0,#marrom
	]
    cores = np.array(cores, dtype=np.float32)
    cvbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, cvbo)
    glBufferData(GL_ARRAY_BUFFER, cores, GL_STATIC_DRAW)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

def inicializaEstrela():
    global Vao_estrela

    # VAO da estrela
    Vao_estrela = glGenVertexArrays(1)
    glBindVertexArray(Vao_estrela)

    # VBO dos vértices
    points = [
		 # triângulo 1
		-0.75, 0.95, 0.0, #Cima
		-0.85, 0.75, 0.0, #vertice inferior direito
		-0.65, 0.75, 0.0, #vertice inferior esquerdo
        #triângulo 2
        -0.75, 0.68, 0.0, #Baixo
        -0.85, 0.9, 0.0, #vertice inferior direito
		-0.65, 0.9, 0.0 #vertice inferior esquerdo
	]

    points = np.array(points, dtype=np.float32)

    pvbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, pvbo)
    glBufferData(GL_ARRAY_BUFFER, points, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)


    # VBO das cores
    cores = [
		#triângulo 1
		1.0, 0.0, 1.0,#magenta
		1.0, 0.0, 1.0,#magenta
        1.0, 0.0, 1.0,#magenta
        #triângulo 2
		1.0, 0.0, 1.0,#magenta
        1.0, 0.0, 1.0,#magenta
        1.0, 0.0, 1.0,#magenta
	]

    cores = np.array(cores, dtype=np.float32)
    cvbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, cvbo)
    glBufferData(GL_ARRAY_BUFFER, cores, GL_STATIC_DRAW)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

def inicializaArvore():
    global Vao_arvore
    # Vao da árvore
    Vao_arvore = glGenVertexArrays(1)
    glBindVertexArray(Vao_arvore)

    # VBO dos vértices da árvore
    points = [
        # triângulo 1
		0.85, 0.25, 0.0, #vertice superior direito
		0.85, -0.5, 0.0, #vertice inferior direito
		0.75, -0.5, 0.0, #vertice inferior esquerdo
		#triângulo 2
		0.75, 0.25, 0.0, #vertice superior esquerdo
		0.85, 0.25, 0.0, #vertice superior direito
		0.75, -0.5, 0.0, #vertice inferior esquerdo
        #triângulo 3
        1.0, 0.25, 0.0, #vertice superior direito
        0.60, 0.25, 0.0, #vertice superior esquerdo
        0.80, 0.75, 0.0  #telhado
	]
    points = np.array(points, dtype=np.float32)
    pvbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, pvbo)
    glBufferData(GL_ARRAY_BUFFER, points, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)


    # VBO das cores
    cores = [
		#triângulo 1
		0.6, 0.3, 0.0,#marrom
		0.6, 0.3, 0.0,
		0.6, 0.3, 0.0,
		#triângulo 2
		0.6, 0.3, 0.0,#marrom
		0.6, 0.3, 0.0,
		0.6, 0.3, 0.0,
        #triângulo 3
        0.0, 1.0, 0.0, #Verde
        0.0, 1.0, 0.0,
        0.0, 1.0, 0.0
	]
    cores = np.array(cores, dtype=np.float32)
    cvbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, cvbo)
    glBufferData(GL_ARRAY_BUFFER, cores, GL_STATIC_DRAW)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

def inicializaShaders():
    global Shader_programm
    # Especificação do Vertex Shader:
    vertex_shader = """
        #version 400
        layout(location = 0) in vec3 vertex_posicao;
        layout(location = 1) in vec3 vertex_cores;
        out vec3 cores;
        void main () {
            cores = vertex_cores;
            gl_Position = vec4 (vertex_posicao.x, vertex_posicao.y, vertex_posicao.z, 1.0);
        }
    """
    vs = OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER)
    if not glGetShaderiv(vs, GL_COMPILE_STATUS):
        infoLog = glGetShaderInfoLog(vs, 512, None)
        print("Erro no vertex shader:\n", infoLog)

    # Especificação do Fragment Shader:
    fragment_shader = """
        #version 400
        in vec3 cores;
		out vec4 frag_colour;
		void main () {
		    frag_colour = vec4 (cores, 1.0);
		}
    """
    fs = OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    if not glGetShaderiv(fs, GL_COMPILE_STATUS):
        infoLog = glGetShaderInfoLog(fs, 512, None)
        print("Erro no fragment shader:\n", infoLog)

    # Especificação do Shader Programm:
    Shader_programm = OpenGL.GL.shaders.compileProgram(vs, fs)
    if not glGetProgramiv(Shader_programm, GL_LINK_STATUS):
        infoLog = glGetProgramInfoLog(Shader_programm, 512, None)
        print("Erro na linkagem do shader:\n", infoLog)

    glDeleteShader(vs)
    glDeleteShader(fs)

def inicializaRenderizacao():
    global Window, Shader_programm, Vao, WIDTH, HEIGHT

    while not glfw.window_should_close(Window):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glViewport(0, 0, WIDTH, HEIGHT)

        glUseProgram(Shader_programm) #ativa o shader

        #desenha a estrela
        glBindVertexArray(Vao_estrela)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        #desenha a árvore
        glBindVertexArray(Vao_arvore)
        glDrawArrays(GL_TRIANGLES, 0, 9)

        #desenha a casa
        glBindVertexArray(Vao_casa)
        glDrawArrays(GL_TRIANGLES, 0, 15)

        glfw.poll_events() #recebe eventos de mouse e teclado

        glfw.swap_buffers(Window) #realiza a troca de buffers para renderizar de fato o que foi desenhado acima
        
        if (glfw.PRESS == glfw.get_key(Window, glfw.KEY_ESCAPE)): #trata os eventos de mouse e teclado
            glfw.set_window_should_close(Window, True)
    
    glfw.terminate()

# Função principal
def main():
    inicializaOpenGL()
    inicializaEstrela() #modelagem da estrela
    inicializaArvore() #modelagem da árvore
    inicializaCasa() #modelagem da casa
    inicializaShaders()
    inicializaRenderizacao()

if __name__ == "__main__":
    main()