rodando = True

def pausar():
    global rodando
    rodando = False

def iniciar():
    global rodando
    rodando = True

def status():
    return rodando