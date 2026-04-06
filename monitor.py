import random
import datetime

def menu():
    nome_arq = 'log.txt'
    while True:
        print('Monitor LogPy')
        print('1 - Gerar logs')
        print('2 - Analisar logs')
        print('3 - Gerar e Analisar logs')
        print('4 - Sair')
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            try:
                qtd = int(input('Quantidade de logs: '))
                gerarArquivo(nome_arq, qtd)
            except:
                print('Quantidade incorreta')
        elif opcao == '2':
            analisarLog(nome_arq)
        elif opcao == '3':
            try:
                qtd = int(input('Quantidade de logs: '))
                gerarArquivo(nome_arq, qtd)
                analisarLog(nome_arq)
            except:
                print('Quantidade incorreta')
        elif opcao == '4':
            print('Até mais')
            break
        else:
            print('Opção errada')
            
def gerarArquivo(nome_arq, qtd):
    with open(nome_arq, 'w', encoding='UTF-8') as arq:
        for i in range(qtd):
            arq.write(montarLog(i) + '\n')
    
    print('Logs gerados')
            
def montarLog(i):
    data = gerarDataHora(i)
    ip = gerarIp(i)
    recurso = gerarRecurso(i)
    metodo = gerarMetodo(i)
    status = gerarStatus(i)
    tempo = gerarTempo(i)
    agente = gerarAgente(i)
    return f'[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - 512B - HTTP/1.1 - {agente} - /home'

def gerarDataHora(i):
    base = datetime.datetime(2026, 3, 30, 22, 8, 0)
    incremento = datetime.timedelta(seconds=i * random.randint(5,20))
    return (base + incremento).strftime('%d/%m/%Y %H:%M:%S')

def gerarIp(i):
    r = random.randint(1, 6)
    
    if i >= 20 and i <= 30:
        return '200.0.111.20'
    
    if r == 1:
        return '192.168.5.6'
    elif r == 2:
        return '139.485.10.0'
    elif r == 3:    
        return '182.485.11.0'
    elif r == 4:    
        return '196.485.12.0'
    elif r == 5:    
        return '177.485.13.0'
    else:    
        return '166.485.14.0'
                                
def gerarRecurso(i):
    r = random.randint(1, 5)
    
    if r == 1:
        return '/home'
    elif r == 2:
        return '/login'
    elif r == 3:
        return '/admin'
    elif r == 4:
        return '/produtos'
    else:
        return '/config'
    
def gerarMetodo(i):
    r = random.randint(1, 2)
    
    if r == 1:
        return 'GET'
    else:
        return 'POST'

def gerarStatus(i):
    r = random.randint(1, 10)
    
    if r <= 5:
        return 200
    elif r <= 7:
        return 403
    elif r <= 9:
        return 404
    else:
        return 500

def gerarTempo(i):
    return random.randint(50, 1000)            

def gerarAgente(i):
    r = random.randint(1, 4)
    
    if r == 1:
        return 'Chrome'
    elif r == 2:
        return 'Firefox'
    elif r == 3:
        return 'Bot'
    else:
        return 'Crawler'
                            
def extrairStatus(linha):
    contador = 0
    campo = ''
    lendo = False
    
    for c in linha:
        if c == '-':
            contador += 1
            continue
        
        if contador == 2:
            if c != ' ':
                campo += c
                lendo = True
            elif lendo:
                break
                
    return int(campo)            

def analisarLog(nome_arq):
    try:
        arq = open(nome_arq, 'r')
    except:
        print('Erro ao abrir arquivo')
        return
    
    total = 0
    sucessos = 0
    erros = 0
    somaTempo = 0
    maiorTempo = 0
    menorTempo = 999999
    rapido = 0
    normal = 0
    lento = 0
    status200 = 0
    status403 = 0
    status404 = 0
    status500 = 0
    ipSuspeito = 0
    errosSeguidos = 0
    maiorSequenciaErro = 0
    home = 0
    login = 0
    admin = 0
    produtos = 0
    config = 0
    adminInvalido = 0
    erros500Seguidos = 0
    falhaCritica = 0
    ipAnterior = ''
    contadorIp = 0
    bot = 0
    ultimoBot = ''
    forcaBruta = 0
    seqLoginErro = 0
    ipAtualFB = ''
    ultimoForcaBruta = ''
    degradacao = 0
    t1 = t2 = t3 = 0
    rotasSens = 0
    falhasSens = 0
    ip1 = '192.168.5.6'
    ip2 = '139.485.10.0'
    ip3 = '182.485.11.0'
    ip4 = '196.485.12.0'
    ip5 = '177.485.13.0'
    ip6 = '166.485.14.0'
    ipSus = '200.0.111.20'
    c1 = c2 = c3 = c4 = c5 = c6 = cSus = 0
    
    for linha in arq:
        total += 1
        
        recurso = extrairRecurso(linha)
        agente = extrairAgente(linha)
        status = extrairStatus(linha)
        ip = extrairIp(linha)
        
        if recurso == '/admin' or recurso == '/config':
            rotasSens += 1
            if status != 200:
                falhasSens += 1
        if recurso == '/login' and status == 403:
            if ip == ipAtualFB:
                seqLoginErro += 1
                if seqLoginErro == 3:
                    forcaBruta += 1
                    ultimoForcaBruta = ip
            else:
                ipAtualFB = ip
                seqLoginErro = 1
        else:
            if ip != ipAtualFB:
                seqLoginErro = 0
        if ip == ipAnterior:
            contadorIp += 1
            if contadorIp == 5:
                bot += 1
                ultimoBot = ip
        else:
            contadorIp = 1
            ipAnterior = ip
        if status == 500:
            erros500Seguidos += 1
            if erros500Seguidos == 3:
                falhaCritica += 1
        else:
            erros500Seguidos = 0
        if recurso == '/admin' and status != 200:
            adminInvalido += 1
        if recurso == '/home':
            home += 1
        elif recurso == '/login':
            login += 1
        elif recurso == '/admin':
            admin += 1
        elif recurso == '/produtos':
            produtos += 1
        elif recurso == '/config':
            config += 1
        if ip == '200.0.111.20':
            ipSuspeito += 1
        if ip == ip1:
            c1 += 1
        elif ip == ip2:
            c2 += 1
        elif ip == ip3:
            c3 += 1
        elif ip == ip4:
            c4 += 1
        elif ip == ip5:
            c5 += 1
        elif ip == ip6:
            c6 += 1
        elif ip == ipSus:
            cSus += 1    
        if status == 200:
            status200 += 1
        elif status == 403:
            status403 += 1
        elif status == 404:
            status404 += 1
        elif status == 500:
            status500 += 1 
        if status != 200:
            errosSeguidos += 1
        else:
            if errosSeguidos > maiorSequenciaErro:
                maiorSequenciaErro = errosSeguidos
            errosSeguidos = 0  

        tempo = extrairTempo(linha)

        somaTempo += tempo

        t1 = t2
        t2 = t3
        t3 = tempo

        if t1 < t2 and t2 < t3:
            degradacao += 1
        if tempo > maiorTempo:
            maiorTempo = tempo
        if tempo < menorTempo:
            menorTempo = tempo
        if tempo < 200:
            rapido += 1
        elif tempo < 800:
            normal += 1
        else:
            lento += 1        
        if status == 200:
            sucessos += 1
        else:
            erros += 1
    
    if total > 0:
        media = somaTempo / total
    else:
        media = 0

    if errosSeguidos > maiorSequenciaErro:
        maiorSequenciaErro = errosSeguidos
    
    disponibilidade = (sucessos / total) * 100
    taxaErro = (erros / total) * 100
    
    maisAcessado = '/home'
    maiorRecurso = home

    if login > maiorRecurso:
        maiorRecurso = login
        maisAcessado = '/login'
    if admin > maiorRecurso:
        maiorRecurso = admin
        maisAcessado = '/admin'
    if produtos > maiorRecurso:
        maiorRecurso = produtos
        maisAcessado = '/produtos'
    if config > maiorRecurso:
        maiorRecurso = config
        maisAcessado = '/config'
    
    if falhaCritica > 0 or disponibilidade < 70:
        estado = 'CRÍTICO'
    elif disponibilidade < 85 or lento > (total * 0.3):
        estado = 'INSTÁVEL'
    elif disponibilidade < 95 or bot > 0:
        estado = 'ATENÇÃO'
    else:
        estado = 'SAUDÁVEL'

    ipMaisAtivo = ip1
    maior = c1

    if c2 > maior:
        maior = c2
        ipMaisAtivo = ip2
    if c3 > maior:
        maior = c3
        ipMaisAtivo = ip3
    if c4 > maior:
        maior = c4
        ipMaisAtivo = ip4
    if c5 > maior:
        maior = c5
        ipMaisAtivo = ip5
    if c6 > maior:
        maior = c6
        ipMaisAtivo = ip6
    if cSus > maior:
        maior = cSus
        ipMaisAtivo = ipSus    
    
    arq.close()
    
    print('Total de acessos:', total)
    print('Total de sucessos:', sucessos)
    print('Total de erros:', erros) 
    print('Tempo médio:', media)
    print('Maior tempo:', maiorTempo)
    print('Menor tempo:', menorTempo)
    print('Acessos rápidos:', rapido)
    print('Acessos normais:', normal)
    print('Acessos lentos:', lento)
    print('Status 200:', status200)
    print('Status 403:', status403)
    print('Status 404:', status404)
    print('Status 500 (críticos):', status500)      
    print('Acessos do IP suspeito:', ipSuspeito)
    print('Maior sequência de erros:', maiorSequenciaErro)
    print('Disponibilidade:', disponibilidade)
    print('Taxa de erro:', taxaErro)
    print('Recurso mais acessado:', maisAcessado)
    print('Acessos indevidos ao /admin:', adminInvalido)
    print('Falhas críticas:', falhaCritica)
    print('Suspeitas de bot:', bot)
    print('Último IP suspeito:', ultimoBot)
    print('Estado do sistema:', estado)
    print('Eventos de força bruta:', forcaBruta)
    print('Último IP força bruta:', ultimoForcaBruta)
    print('Eventos de degradação:', degradacao)
    print('Acessos a rotas sensíveis:', rotasSens)
    print('Falhas em rotas sensíveis:', falhasSens)
    print('IP mais ativo:', ipMaisAtivo)


def extrairIp(linha):
    ip = ''
    lendo = False
    
    for c in linha:
        if c == ']':
            lendo = True
            continue
        
        if lendo:
            if c != ' ':
                ip += c
            else:
                break
    
    return ip

def extrairTempo(linha):
    contador = 0
    campo = ''
    lendo = False
    
    for c in linha:
        if c == '-':
            contador += 1
            continue
        
        if contador == 4:
            if c.isdigit():
                campo += c
                lendo = True
            elif lendo:
                break
    
    return int(campo)

def extrairRecurso(linha):
    contador = 0
    campo = ''
    lendo = False

    for c in linha:
        if c == '-':
            contador += 1
            continue
        
        if contador == 3:
            if c != ' ':
                campo += c
                lendo = True
            elif lendo:
                break
    
    return campo

def extrairAgente(linha):
    contador = 0
    campo = ''
    lendo = False

    for c in linha:
        if c == '-':
            contador += 1
            continue
        
        if contador == 7:
            if c != ' ':
                campo += c
                lendo = True
            elif lendo:
                break
    
    return campo    

menu()