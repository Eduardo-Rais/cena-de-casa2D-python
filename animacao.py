import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np

Window = None
Shader_programm = None
Vao_triangulo = None
Vao_quadrado = None
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

def inicializaTriangulo():
    global Vao_triangulo

    # VAO do triângulo
    Vao_triangulo = glGenVertexArrays(1)
    glBindVertexArray(Vao_triangulo)

    # VBO dos vértices
    points = [
		 # triângulo 1
		0.5, -0.5, 0.0, #vertice superior direito
		0.0, 0.5, 0.0, #vertice inferior direito
		-0.5, -0.5, 0.0, #vertice inferior esquerdo
	]

    points = np.array(points, dtype=np.float32)

    pvbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, pvbo)
    glBufferData(GL_ARRAY_BUFFER, points, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

def inicializaQuadrado():
    global Vao_quadrado

    # VAO do quadrado
    Vao_quadrado = glGenVertexArrays(1)
    glBindVertexArray(Vao_quadrado)

    # VBO dos vértices
    points = [
		# triângulo 1
		0.5, 0.5, 0.0, #vertice superior direito
		0.5, -0.5, 0.0, #vertice inferior direito
		-0.5, -0.5, 0.0, #vertice inferior esquerdo
		#triângulo 2
		-0.5, 0.5, 0.0, #vertice superior esquerdo
		0.5, 0.5, 0.0, #vertice superior direito
		-0.5, -0.5, 0.0 #vertice inferior esquerdo
	]

    points = np.array(points, dtype=np.float32)

    pvbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, pvbo)
    glBufferData(GL_ARRAY_BUFFER, points, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

def inicializaShaders():
    global Shader_programm
    # Especificação do Vertex Shader:
    vertex_shader = """
        #version 400
        layout(location = 0) in vec3 vertex_posicao;
        //Variável que receberá uma matriz de transformação geométrica
        uniform mat4 transform;
        void main () {
            //multiplicamos a matriz "transform" pelo vértice do modelo do objeto
            gl_Position = transform * vec4 (vertex_posicao, 1.0);
        }
    """
    vs = OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER)
    if not glGetShaderiv(vs, GL_COMPILE_STATUS):
        infoLog = glGetShaderInfoLog(vs, 512, None)
        print("Erro no vertex shader:\n", infoLog)

    # Especificação do Fragment Shader:
    fragment_shader = """
        #version 400
		out vec4 frag_colour;
        uniform vec4 cor;
		void main () {
		    frag_colour = cor;
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

def trocaCor(r, g, b, a):
    #transformo o r,g,b,a em um array
    cor = np.array([r, g, b, a]) 
    #busca a localização da variável "cor" no shader/memória de vídeo
    corLocalizacao = glGetUniformLocation(Shader_programm, "cor")
    #copia os valores da variavel "cor" do python para a variável "cor" do shader
    glUniform4fv(corLocalizacao, 1, cor)

def transformacaoGeometrica(tx, ty, tz, sx, sy, sz, rx, ry, rz):
    #matriz de translação
    translacao = np.array([
        [1.0, 0.0, 0.0, tx],
        [0.0, 1.0, 0.0, ty],
        [0.0, 0.0, 1.0, tz], 
        [0.0, 0.0, 0.0, 1.0]], np.float32)
    
    #matriz de escala
    escala = np.array([
        [sx, 0.0, 0.0, 0.0],
        [0.0, sy, 0.0, 0.0],
        [0.0, 0.0, sz, 0.0], 
        [0.0, 0.0, 0.0, 1.0]], np.float32)
    
    #matriz de rotação em X
    angulo = np.radians(rx)
    cos = np.cos(angulo)
    sen = np.sin(angulo)
    rotacaoX = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, cos, -sen, 0.0],
        [0.0, sen, cos, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])

    #matriz de rotação em Y
    angulo = np.radians(ry)
    cos = np.cos(angulo)
    sen = np.sin(angulo)
    rotacaoY = np.array([
        [cos, 0.0, sen, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [-sen, 0.0, cos, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])

    #matriz de rotação em Z
    angulo = np.radians(rz)
    cos = np.cos(angulo)
    sen = np.sin(angulo)
    rotacaoZ = np.array([
        [cos, -sen, 0.0, 0.0],
        [sen, cos, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])

    #combina todas as trasnformações em uma única matriz
    transform = escala @ rotacaoX @ rotacaoY @ rotacaoZ @ translacao

    #busca a localização da variável "trasnform" no shader/memória de vídeo
    transformLocalizacao = glGetUniformLocation(Shader_programm, "transform")
    
    #copia os valores da variavel "transform" do python para a variável "transform" do shader
    #GL_TRUE indica que é pra transpor a matriz, pois o shader/glsl trabalha no modo "coluna-linha", e o python é "linha-coluna"
    glUniformMatrix4fv(transformLocalizacao, 1, GL_TRUE, transform)


def inicializaRenderizacao():
    global Window, Shader_programm, Vao, WIDTH, HEIGHT
    tini = glfw.get_time() #variável para controlar o tempo de execução do programa

    while not glfw.window_should_close(Window):
        tfim = glfw.get_time()
        tini = tfim

        anguloSol = tini*100%360
        fator = (np.sin(np.radians(anguloSol)) +1)/2

        r = fator * (0.6)
        g = fator * (0.85)
        b = 0.15 + fator * (0.92 - 0.02)

        glClearColor(r, g, b, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glViewport(0, 0, WIDTH, HEIGHT)

        glUseProgram(Shader_programm) #ativa o shader

        #desenha o chao
        glBindVertexArray(Vao_quadrado)
        trocaCor(55/255, 125/255, 34/255, 1.0)
        transformacaoGeometrica(0,-0.5,0,2,1,1,0,0,0)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        #desenha sol
        glBindVertexArray(Vao_quadrado)
        trocaCor(1.0, 1.0, 0.0, 1.0) #amarelo
        if anguloSol < 150:
            transformacaoGeometrica(3.5, 1, 0, 0.2, 0.25, 1, 0, 0, anguloSol)
            glDrawArrays(GL_TRIANGLES, 0, 6)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0) #preto

        #desenha casa
        trocaCor(1.0, 1.0, 1.0, 1.0) #branco
        transformacaoGeometrica(-0.25, 0, 0, 1.25, 1, 1, 0, 0, 0)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        #desenha a porta
        trocaCor(0.5, 0.25, 0.0, 1.0) #marrom
        transformacaoGeometrica(-0.25, -0.25, 0, 0.25, 0.5, 1, 0, 0, 0)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        #desenha a janela
        trocaCor(0.0, 0.5, 1.0, 1.0) #azul
        transformacaoGeometrica(-2, 0, 0, 0.25, 0.25, 1, 0, 0, 0)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        #desenha arvore
        trocaCor(0.5, 0.25, 0.0, 1.0) #marrom
        transformacaoGeometrica(7, -0.25, 0, 0.1, 0.65, 1, 0, 0, 0)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        #desenha o telhado
        glBindVertexArray(Vao_triangulo)
        trocaCor(1.0, 0.0, 0.0, 1.0) #vermelho
        transformacaoGeometrica(-0.25, 1.5, 0, 1.25, 0.5, 1, 0, 0, 0)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        #desenha a copa da arvore
        trocaCor(0.0, 0.5, 0.0, 1.0) #verde
        transformacaoGeometrica(1.4, 0.7, 0, 0.5, 0.5, 1, 0, 0, 0)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glfw.poll_events() #recebe eventos de mouse e teclado

        glfw.swap_buffers(Window) #realiza a troca de buffers para renderizar de fato o que foi desenhado acima
        
        if (glfw.PRESS == glfw.get_key(Window, glfw.KEY_ESCAPE)): #trata os eventos de mouse e teclado
            glfw.set_window_should_close(Window, True)
    
    glfw.terminate()

# Função principal
def main():
    inicializaOpenGL()
    inicializaTriangulo() #modelagem do triângulo
    inicializaQuadrado() #modelagem do quadrado
    inicializaShaders()
    inicializaRenderizacao()

if __name__ == "__main__":
    main()