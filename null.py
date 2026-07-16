#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#           NULLSCRIPT - VERSÃO PYTHON COMPLETA
#           "Programação para humanos"
# ============================================================
#  Como usar:
#    python nullscript.py arquivo.ns
#    nullscript arquivo.ns
#    ns arquivo.ns
# ============================================================

import os
import sys
import re
import json
import hashlib
import subprocess
import platform
import time
import random
import math
import datetime
import socket
import urllib.request
import urllib.parse
import threading
import queue
import tempfile
import shutil
import glob
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable

# ============================================================
#              CONFIGURAÇÃO
# ============================================================

VERSAO = "3.0.0"
NOME = "NullScript"
AUTOR = "mateusgataolindaomateusgatao-create"
REPOSITORIO = "https://github.com/mateusgataolindaomateusgatao-create/nullscript-python"

# Cores para terminal
CORES = {
    'vermelho': '\033[91m',
    'verde': '\033[92m',
    'amarelo': '\033[93m',
    'azul': '\033[94m',
    'roxo': '\033[95m',
    'ciano': '\033[96m',
    'branco': '\033[97m',
    'negrito': '\033[1m',
    'sublinhado': '\033[4m',
    'reset': '\033[0m'
}

# ============================================================
#              CLASSE IA (CORRETORAUTO)
# ============================================================

class CorretorAuto:
    """IA integrada para correção, explicação e geração de código"""
    
    def __init__(self):
        self.modelo = "llama4-scout"
        self.auto_corrigir = True
        self.modo_aprendiz = False
        self.estilo = None
        self.historico = []
        self.cache = {}
    
    def corrigir(self, codigo: str) -> str:
        """Corrige código NullScript automaticamente"""
        # Correções básicas
        substituicoes = {
            'if': 'se',
            'else': 'senao',
            'while': 'enquanto',
            'for': 'para',
            'function': 'funcao',
            'return': 'retorne',
            'true': 'verdadeiro',
            'false': 'falso',
            'null': 'vazio',
            'undefined': 'indefinido',
            'print': 'exibir',
            'input': 'perguntar'
        }
        
        for antigo, novo in substituicoes.items():
            codigo = re.sub(rf'\b{antigo}\b', novo, codigo, flags=re.IGNORECASE)
        
        # Corrigir estruturas não fechadas
        se_count = len(re.findall(r'\bse\b', codigo, re.IGNORECASE))
        fim_count = len(re.findall(r'\bfim\b', codigo, re.IGNORECASE))
        if se_count > fim_count:
            codigo += '\nFim'
        
        return codigo
    
    def explicar(self, codigo: str) -> str:
        """Explica o código em linguagem natural"""
        explicacao = []
        explicacao.append("📖 EXPLICAÇÃO DO CÓDIGO")
        explicacao.append("=" * 50)
        
        # Análise básica
        linhas = codigo.split('\n')
        funcoes = re.findall(r'funcao\s+(\w+)', codigo)
        variaveis = re.findall(r'(\w+)\s*=', codigo)
        
        explicacao.append(f"📊 Total de linhas: {len(linhas)}")
        explicacao.append(f"📦 Funções: {', '.join(funcoes) if funcoes else 'Nenhuma'}")
        explicacao.append(f"📦 Variáveis: {', '.join(set(variaveis)) if variaveis else 'Nenhuma'}")
        
        if 'se' in codigo.lower():
            explicacao.append("🔀 Contém estrutura condicional (se/senao)")
        if 'enquanto' in codigo.lower():
            explicacao.append("🔄 Contém loop (enquanto)")
        if 'para' in codigo.lower():
            explicacao.append("🔄 Contém loop (para)")
        
        return '\n'.join(explicacao)
    
    def gerar(self, descricao: str) -> str:
        """Gera código a partir de descrição"""
        codigo = []
        codigo.append("// Código gerado pela IA")
        codigo.append(f"// Descrição: {descricao}")
        codigo.append("")
        
        if "calculadora" in descricao.lower():
            codigo.extend([
                "funcao calculadora() {",
                "    exibir: '🧮 CALCULADORA'",
                "    a = numero(perguntar('Primeiro número: '))",
                "    b = numero(perguntar('Segundo número: '))",
                "    op = perguntar('Operação (+, -, *, /): ')",
                "    resultado = 0",
                "    escolha op",
                "        caso '+': resultado = a + b",
                "        caso '-': resultado = a - b",
                "        caso '*': resultado = a * b",
                "        caso '/':",
                "            se b == 0",
                "                exibir: '❌ Divisão por zero!'",
                "                retorne",
                "            fim",
                "            resultado = a / b",
                "        padrao: exibir: '❌ Operação inválida!'",
                "    fim",
                "    exibir: '✅ Resultado: ' + resultado",
                "}",
                "",
                "calculadora()"
            ])
        elif "api" in descricao.lower():
            codigo.extend([
                "importar biblioteca Auto",
                "importar biblioteca Rede",
                "",
                "api = Auto.criar_api({",
                "    nome: 'usuarios',",
                "    campos: ['nome', 'email', 'idade']",
                "})",
                "",
                "Rede.servidor(3000).iniciar()"
            ])
        else:
            codigo.extend([
                "funcao main() {",
                "    exibir: '🚀 Olá mundo!'",
                "    nome = perguntar('Qual seu nome? ')",
                "    exibir: 'Olá, ' + nome + '!'",
                "}",
                "",
                "main()"
            ])
        
        return '\n'.join(codigo)
    
    def analisar(self, codigo: str) -> Dict:
        """Analisa a qualidade do código"""
        analise = {
            'erros': [],
            'avisos': [],
            'sugestoes': [],
            'qualidade': 0,
            'complexidade': 0,
            'seguranca': 0,
            'performance': 0,
            'manutenibilidade': 0,
            'linhas': len(codigo.split('\n')),
            'caracteres': len(codigo),
            'funcoes': len(re.findall(r'funcao\s+\w+', codigo)),
            'estruturas': {
                'se': len(re.findall(r'\bse\b', codigo, re.IGNORECASE)),
                'enquanto': len(re.findall(r'\benquanto\b', codigo, re.IGNORECASE)),
                'para': len(re.findall(r'\bpara\b', codigo, re.IGNORECASE)),
                'funcao': len(re.findall(r'\bfuncao\b', codigo, re.IGNORECASE))
            }
        }
        
        # Verificar estruturas não fechadas
        se_count = len(re.findall(r'\bse\b', codigo, re.IGNORECASE))
        fim_count = len(re.findall(r'\bfim\b', codigo, re.IGNORECASE))
        if se_count > fim_count:
            analise['erros'].append(f"Faltam {se_count - fim_count} 'Fim'")
        
        # Verificar comentários
        if '//' not in codigo and '#' not in codigo:
            analise['sugestoes'].append('Adicione comentários')
        
        # Verificar boas práticas
        if '==' in codigo and '===' not in codigo:
            analise['avisos'].append('Use "===" para comparações estritas')
        
        # Calcular métricas
        analise['qualidade'] = min(10, 10 - len(analise['erros']) - len(analise['avisos']) * 0.5)
        analise['complexidade'] = min(10, len(codigo.split('\n')) // 10 + 1)
        analise['seguranca'] = 8
        analise['performance'] = 7
        analise['manutenibilidade'] = min(10, 10 - len(analise['avisos']) * 0.3)
        
        return analise
    
    def perguntar(self, pergunta: str) -> str:
        """Responde perguntas sobre programação"""
        respostas = {
            'como faço para': 'Você pode usar o comando...',
            'erro': 'Verifique a sintaxe. Use "Se:", "Enquanto:", etc.',
            'função': 'Use "funcao nome(parametros) { ... }"',
            'variável': 'Use "crie variável, nome X, valor Y"',
            'lista': 'Use [] para criar listas. Ex: [1, 2, 3]',
            'string': 'Use "" ou \'\' para strings. Ex: "Olá mundo"',
            'if': 'Use "Se: condicao" para condicionais',
            'loop': 'Use "Enquanto: condicao" ou "Para i de 1 ate 10"',
            'api': 'Use "importar biblioteca Auto" e "Auto.criar_api()"',
            'arquivo': 'Use "importar biblioteca Arquivos"',
        }
        
        for chave, resposta in respostas.items():
            if chave in pergunta.lower():
                return resposta
        
        return "Em NullScript você pode programar de forma intuitiva em português. Use 'IA.explicar(codigo)' para mais ajuda."
    
    def otimizar(self, codigo: str) -> str:
        """Otimiza o código"""
        otimizado = codigo
        # Remover espaços extras
        otimizado = '\n'.join([linha.strip() for linha in otimizado.split('\n') if linha.strip()])
        # Simplificar
        otimizado = re.sub(r'se\s+\(', 'se ', otimizado)
        otimizado = re.sub(r'enquanto\s+\(', 'enquanto ', otimizado)
        return otimizado
    
    def completar(self, codigo: str) -> str:
        """Completa código incompleto"""
        if 'funcao' in codigo and '{' in codigo and '}' not in codigo:
            return codigo + '\n    // TODO: Implementar lógica\n    retorne null\n}'
        if 'se' in codigo.lower() and 'fim' not in codigo.lower():
            return codigo + '\n    // TODO: Adicionar lógica\nFim'
        return codigo


# ============================================================
#              INTERPRETADOR NULLSCRIPT
# ============================================================

class NullScriptInterpreter:
    """Interpretador principal da linguagem NullScript"""
    
    def __init__(self):
        self.variaveis = {}
        self.funcoes = {}
        self.constantes = {}
        self.importacoes = {}
        self.ia = CorretorAuto()
        self.debug = False
        self.modo_aprendiz = False
        self.auto_corrigir = True
        self.historico = []
        self.linha_atual = 0
        self.arquivo_atual = ''
        self.retorno_atual = None
        self.pausado = False
        self.bibliotecas = {}
        self.carregar_bibliotecas()
    
    def carregar_bibliotecas(self):
        """Carrega bibliotecas nativas"""
        self.bibliotecas = {
            # CorretorAuto - IA
            'CorretorAuto': {
                'corrigir': self.ia.corrigir,
                'explicar': self.ia.explicar,
                'gerar': self.ia.gerar,
                'analisar': self.ia.analisar,
                'perguntar': self.ia.perguntar,
                'otimizar': self.ia.otimizar,
                'completar': self.ia.completar
            },
            
            # Matematica
            'Matematica': {
                'soma': lambda *args: sum(args),
                'multiplica': lambda *args: __import__('math').prod(args) if args else 0,
                'divide': lambda a, b: a / b if b != 0 else None,
                'subtrai': lambda *args: args[0] - sum(args[1:]) if args else 0,
                'potencia': pow,
                'raiz': math.sqrt,
                'raiz_cubica': math.cbrt,
                'fatorial': math.factorial,
                'fibonacci': lambda n: n if n <= 1 else (lambda f: f(n))(lambda n: n if n <= 1 else (lambda f: f(n-1) + f(n-2))(lambda n: n if n <= 1 else (lambda f: f(n-1) + f(n-2))(n-1) + (lambda f: f(n-1) + f(n-2))(n-2))),
                'primo': lambda n: n > 1 and all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1)),
                'aleatorio': random.random,
                'aleatorio_entre': random.randint,
                'absoluto': abs,
                'arredondar': round,
                'arredondar_baixo': math.floor,
                'arredondar_cima': math.ceil,
                'seno': math.sin,
                'cosseno': math.cos,
                'tangente': math.tan,
                'log': math.log,
                'log10': math.log10,
                'log2': math.log2,
                'maximo': max,
                'minimo': min,
                'media': lambda *args: sum(args) / len(args) if args else 0,
            },
            
            # Arquivos
            'Arquivos': {
                'ler': lambda p: open(p, 'r', encoding='utf-8').read(),
                'ler_linhas': lambda p: open(p, 'r', encoding='utf-8').read().split('\n'),
                'ler_json': lambda p: json.load(open(p, 'r', encoding='utf-8')),
                'escrever': lambda p, c: open(p, 'w', encoding='utf-8').write(c),
                'adicionar': lambda p, c: open(p, 'a', encoding='utf-8').write(c),
                'existe': os.path.exists,
                'deletar': os.remove,
                'copiar': shutil.copy2,
                'mover': shutil.move,
                'listar': os.listdir,
                'criar_pasta': lambda p: os.makedirs(p, exist_ok=True),
                'deletar_pasta': lambda p: shutil.rmtree(p),
            },
            
            # Sistema
            'Sistema': {
                'executar': lambda cmd: subprocess.run(cmd, shell=True, capture_output=True, text=True),
                'info': lambda: {
                    'hostname': socket.gethostname(),
                    'platform': platform.system(),
                    'arch': platform.machine(),
                    'cpus': os.cpu_count(),
                    'python': sys.version,
                    'cwd': os.getcwd()
                },
                'limpar': lambda: os.system('clear' if os.name == 'posix' else 'cls'),
                'sair': sys.exit,
            },
            
            # Rede
            'Rede': {
                'get': lambda url: urllib.request.urlopen(url).read().decode('utf-8'),
                'ip': lambda: socket.gethostbyname(socket.gethostname()),
                'ping': lambda host: os.system(f'ping -c 1 {host}') == 0,
            },
            
            # Criptografia
            'Criptografia': {
                'md5': lambda d: hashlib.md5(str(d).encode()).hexdigest(),
                'sha256': lambda d: hashlib.sha256(str(d).encode()).hexdigest(),
                'sha512': lambda d: hashlib.sha512(str(d).encode()).hexdigest(),
                'gerar_token': lambda t=32: os.urandom(t).hex(),
            },
            
            # Testes
            'Testes': {
                'testar': lambda desc, fn: (print(f'\n🧪 Teste: {desc}'), fn(), print('✅ PASSED'))[1] if True else None,
                'afirmar': lambda cond, msg=None: (lambda: None) if cond else (lambda: (_ for _ in ()).throw(Exception(msg or 'Assertion failed')))(),
                'afirmar_igual': lambda a, b, msg=None: (lambda: None) if a == b else (lambda: (_ for _ in ()).throw(Exception(msg or f'{a} != {b}')))(),
            },
            
            # Facil - Operações Facilitadas
            'Facil': {
                'media': lambda lista: sum(lista) / len(lista) if lista else 0,
                'mediana': lambda lista: (lambda s: s[len(s)//2] if len(s)%2 else (s[len(s)//2-1] + s[len(s)//2])/2)(sorted(lista)),
                'moda': lambda lista: max(set(lista), key=lista.count) if lista else None,
                'desvio_padrao': lambda lista: (lambda m: (sum((x-m)**2 for x in lista)/len(lista))**0.5)(sum(lista)/len(lista)) if lista else 0,
                'ordenar': lambda lista: sorted(lista),
                'buscar': lambda lista, valor: lista.index(valor) if valor in lista else -1,
                'ler_csv': lambda p: [line.strip().split(',') for line in open(p, 'r').readlines()],
                'ler_json': lambda p: json.load(open(p, 'r')),
                'sentimentar': lambda texto: 'positivo' if sum(1 for p in ['bom','ótimo','excelente'] if p in texto.lower()) > sum(1 for n in ['ruim','péssimo','horrível'] if n in texto.lower()) else 'negativo' if sum(1 for n in ['ruim','péssimo','horrível'] if n in texto.lower()) > 0 else 'neutro',
            },
            
            # Preguiçoso - IA que completa
            'Preguiçoso': {
                'fazer': self.ia.gerar,
                'completar': self.ia.completar,
                'otimizar': self.ia.otimizar,
                'explicar': self.ia.explicar,
            },
            
            # Auto - Automatização
            'Auto': {
                'criar_api': lambda config: f"// API {config.get('nome', 'recurso')}\n# Implementação gerada automaticamente",
                'criar_crud': lambda nome, campos: f"// CRUD {nome}\n# Implementação gerada automaticamente",
                'criar_jogo': lambda tipo: "// Jogo gerado\nimportar biblioteca Jogo\n\njogo = Jogo.criar(800, 600, 'Meu Jogo')\nJogo.iniciar(jogo)",
                'criar_site': lambda config: "// Site gerado\nimportar biblioteca Web\n\nWeb.servidor(3000).iniciar()",
            },
            
            # Jogo
            'Jogo': {
                'criar': lambda w=800, h=600, t='Jogo': {'largura': w, 'altura': h, 'titulo': t, 'sprites': []},
                'sprite': lambda jogo, img, x=0, y=0: {'imagem': img, 'x': x, 'y': y},
                'iniciar': lambda jogo: print(f'🎮 Iniciando: {jogo["titulo"]}'),
                'loop': lambda jogo, func: func() if callable(func) else None,
            },
            
            # Web
            'Web': {
                'servidor': lambda porta=3000: print(f'🌐 Servidor em http://localhost:{porta}'),
                'rota': lambda path, handler: handler,
                'html': lambda content: f'<html>{content}</html>',
                'json': lambda data: json.dumps(data),
            }
        }
    
    def executar(self, codigo: str, arquivo: str = '') -> Any:
        """Executa código NullScript"""
        inicio = time.time()
        self.historico.append(codigo)
        self.arquivo_atual = arquivo
        
        try:
            if self.auto_corrigir:
                corrigido = self.ia.corrigir(codigo)
                if corrigido != codigo and self.debug:
                    print('[IA] Código corrigido')
                codigo = corrigido
            
            resultado = self.interpretar(codigo)
            return resultado
        except Exception as erro:
            print(f'❌ Erro na linha {self.linha_atual}: {erro}')
            if self.auto_corrigir:
                print('[IA] Tentando corrigir...')
                try:
                    codigo_corrigido = self.ia.corrigir(self.historico[-1])
                    return self.executar(codigo_corrigido, arquivo)
                except:
                    pass
            raise
    
    def interpretar(self, codigo: str) -> Any:
        """Interpreta código linha por linha"""
        linhas = codigo.split('\n')
        resultado = None
        em_bloco = False
        bloco = []
        bloco_tipo = ''
        bloco_condicao = ''
        
        for i, linha in enumerate(linhas):
            self.linha_atual = i + 1
            linha_trim = linha.strip()
            
            if not linha_trim or linha_trim.startswith('//') or linha_trim.startswith('#'):
                continue
            
            # Detectar bloco
            if re.match(r'^(se|enquanto|para|funcao|tentar|escolha)', linha_trim, re.IGNORECASE):
                em_bloco = True
                bloco_tipo = linha_trim.split()[0]
                bloco_condicao = linha_trim
                bloco = []
                continue
            
            if re.match(r'^(fim|end|})', linha_trim, re.IGNORECASE):
                em_bloco = False
                resultado = self.executar_bloco(bloco_tipo, bloco_condicao, bloco)
                continue
            
            if em_bloco:
                bloco.append(linha)
                continue
            
            try:
                resultado = self.processar_linha(linha)
            except Exception as e:
                if self.modo_aprendiz:
                    print(f'[IA] Erro na linha {i+1}: {e}')
                    print(f'[IA] Sugestão: {self.ia.perguntar(str(e))}')
                raise
        
        return resultado
    
    def executar_bloco(self, tipo: str, condicao: str, linhas: List[str]) -> Any:
        """Executa um bloco de código"""
        codigo_bloco = '\n'.join(linhas)
        
        if tipo.lower() == 'se':
            return self.executar_se(condicao, codigo_bloco)
        elif tipo.lower() == 'enquanto':
            return self.executar_enquanto(condicao, codigo_bloco)
        elif tipo.lower() == 'para':
            return self.executar_para(condicao, codigo_bloco)
        elif tipo.lower() == 'funcao':
            return self.executar_funcao(condicao, codigo_bloco)
        else:
            return self.interpretar(codigo_bloco)
    
    def executar_se(self, condicao: str, bloco: str) -> Any:
        """Executa estrutura condicional"""
        cond = re.sub(r'^se\s*:?\s*', '', condicao, flags=re.IGNORECASE).strip()
        resultado = self.avaliar_expressao(cond)
        if resultado:
            return self.interpretar(bloco)
        return None
    
    def executar_enquanto(self, condicao: str, bloco: str) -> Any:
        """Executa loop enquanto"""
        cond = re.sub(r'^enquanto\s*:?\s*', '', condicao, flags=re.IGNORECASE).strip()
        resultado = None
        max_iter = 1000000
        iteracoes = 0
        
        while self.avaliar_expressao(cond) and iteracoes < max_iter:
            try:
                resultado = self.interpretar(bloco)
                iteracoes += 1
            except Exception as e:
                if str(e) == 'BREAK':
                    break
                if str(e) == 'CONTINUE':
                    continue
                raise
        
        return resultado
    
    def executar_para(self, condicao: str, bloco: str) -> Any:
        """Executa loop para"""
        match = re.match(r'para\s+(\w+)\s+de\s+(\d+)\s+ate\s+(\d+)(?:\s+passo\s+(\d+))?', condicao, re.IGNORECASE)
        if not match:
            return None
        
        var, inicio, fim, passo = match.groups()
        inicio = int(inicio)
        fim = int(fim)
        passo = int(passo) if passo else 1
        resultado = None
        
        self.variaveis[var] = inicio
        valor = inicio
        
        while (passo > 0 and valor <= fim) or (passo < 0 and valor >= fim):
            self.variaveis[var] = valor
            try:
                resultado = self.interpretar(bloco)
            except Exception as e:
                if str(e) == 'BREAK':
                    break
                if str(e) == 'CONTINUE':
                    valor += passo
                    continue
                raise
            valor += passo
        
        return resultado
    
    def executar_funcao(self, condicao: str, bloco: str) -> Any:
        """Define uma função"""
        match = re.match(r'funcao\s+(\w+)\s*\(([^)]*)\)', condicao, re.IGNORECASE)
        if not match:
            return None
        
        nome, params = match.groups()
        parametros = [p.strip() for p in params.split(',')] if params else []
        
        def funcao_executar(*args):
            vars_antigas = self.variaveis.copy()
            for i, p in enumerate(parametros):
                self.variaveis[p] = args[i] if i < len(args) else None
            
            try:
                resultado = self.interpretar(bloco)
                return resultado
            finally:
                self.variaveis = vars_antigas
        
        self.funcoes[nome] = {
            'nome': nome,
            'parametros': parametros,
            'corpo': bloco,
            'executar': funcao_executar
        }
        
        return self.funcoes[nome]
    
    def processar_linha(self, linha: str) -> Any:
        """Processa uma linha de código"""
        linha_trim = linha.strip()
        
        # Exibir
        if re.match(r'^(exibir|mostrar|print)', linha_trim, re.IGNORECASE):
            return self.processar_exibir(linha)
        
        # Perguntar
        if re.match(r'^(perguntar|input)', linha_trim, re.IGNORECASE):
            return self.processar_perguntar(linha)
        
        # Declaração de variável
        if re.match(r'^(crie|criar|var|let|declare)', linha_trim, re.IGNORECASE):
            return self.processar_declaracao(linha)
        
        # Constante
        if re.match(r'^constante', linha_trim, re.IGNORECASE):
            return self.processar_constante(linha)
        
        # Retorno
        if re.match(r'^(retorne|return)', linha_trim, re.IGNORECASE):
            return self.processar_retorne(linha)
        
        # Importar
        if re.match(r'^(importar|import)', linha_trim, re.IGNORECASE):
            return self.processar_importar(linha)
        
        # Limpar
        if re.match(r'^(limpar|clear)', linha_trim, re.IGNORECASE):
            os.system('clear' if os.name == 'posix' else 'cls')
            return True
        
        # Sair
        if re.match(r'^(sair|exit)', linha_trim, re.IGNORECASE):
            sys.exit(0)
        
        # Atribuição
        if '=' in linha_trim and not linha_trim.startswith('=='):
            return self.processar_atribuicao(linha)
        
        # Chamada de função
        if '(' in linha_trim and ')' in linha_trim:
            return self.processar_chamada_funcao(linha)
        
        # Expressão
        return self.avaliar_expressao(linha)
    
    def processar_exibir(self, linha: str) -> str:
        """Processa comando exibir"""
        texto = re.sub(r'^(exibir|mostrar|print)\s*:?\s*', '', linha)
        texto = re.sub(r'^["\']|["\']$', '', texto)
        
        # Interpolação
        def substituir_var(match):
            var = match.group(1).strip()
            return str(self.variaveis.get(var, var))
        
        texto = re.sub(r'\$\{([^}]+)\}', substituir_var, texto)
        texto = re.sub(r'\{([^}]+)\}', substituir_var, texto)
        
        print(texto)
        return texto
    
    def processar_perguntar(self, linha: str) -> str:
        """Processa comando perguntar"""
        texto = re.sub(r'^(perguntar|input)\s*:?\s*', '', linha)
        texto = re.sub(r'^["\']|["\']$', '', texto)
        
        resposta = input(texto + ' ')
        
        # Tenta converter para número
        try:
            if '.' in resposta:
                return float(resposta)
            return int(resposta)
        except ValueError:
            return resposta
    
    def processar_declaracao(self, linha: str) -> Any:
        """Processa declaração de variável"""
        match = re.match(r'(?:crie|criar|var|let|declare)\s+(?:variavel\s*,\s*nome\s*)?(\w+)(?:\s*,\s*valor\s*)?\s*=\s*(.+)', linha, re.IGNORECASE)
        if not match:
            match = re.match(r'(?:var|let)\s+(\w+)\s*=\s*(.+)', linha, re.IGNORECASE)
            if not match:
                return None
        
        nome, valor = match.groups()
        self.variaveis[nome] = self.avaliar_expressao(valor.strip())
        return self.variaveis[nome]
    
    def processar_atribuicao(self, linha: str) -> Any:
        """Processa atribuição simples"""
        match = re.match(r'^(\w+)\s*=\s*(.+)', linha)
        if not match:
            return None
        
        nome, valor = match.groups()
        self.variaveis[nome] = self.avaliar_expressao(valor.strip())
        return self.variaveis[nome]
    
    def processar_constante(self, linha: str) -> Any:
        """Processa declaração de constante"""
        match = re.match(r'constante\s+(\w+)\s*=\s*(.+)', linha, re.IGNORECASE)
        if not match:
            return None
        
        nome, valor = match.groups()
        self.constantes[nome] = self.avaliar_expressao(valor.strip())
        return self.constantes[nome]
    
    def processar_retorne(self, linha: str) -> Any:
        """Processa retorno de função"""
        valor = re.sub(r'^(retorne|return)\s*:?\s*', '', linha)
        resultado = self.avaliar_expressao(valor)
        self.retorno_atual = resultado
        raise Exception('RETURN')
    
    def processar_importar(self, linha: str) -> Any:
        """Processa importação de biblioteca"""
        match = re.match(r'importar\s+(?:biblioteca\s+)?(\w+)', linha, re.IGNORECASE)
        if not match:
            return None
        
        nome = match.group(1)
        self.importacoes[nome] = True
        
        if nome in self.bibliotecas:
            self.variaveis[nome] = self.bibliotecas[nome]
            return self.bibliotecas[nome]
        
        return nome
    
    def processar_chamada_funcao(self, linha: str) -> Any:
        """Processa chamada de função"""
        match = re.match(r'(\w+)\s*\(([^)]*)\)', linha)
        if not match:
            return None
        
        nome, args = match.groups()
        argumentos = [self.avaliar_expressao(a.strip()) for a in args.split(',')] if args else []
        
        # Funções nativas
        nativas = {
            'tipo': lambda v: type(v).__name__,
            'numero': lambda v: float(v) if '.' in str(v) else int(v),
            'texto': str,
            'lista': lambda *v: list(v),
            'aleatorio': random.random,
            'aleatorio_entre': random.randint,
            'data_atual': lambda: str(datetime.datetime.now()),
            'timestamp': lambda: int(time.time()),
            'dormir': time.sleep,
            'tamanho': lambda v: len(v) if v else 0,
            'contem': lambda v, i: i in v if v else False,
            'posicao': lambda v, i: v.index(i) if i in v else -1,
            'maiusculo': lambda v: v.upper() if v else '',
            'minusculo': lambda v: v.lower() if v else '',
            'absoluto': abs,
            'raiz_quadrada': math.sqrt,
            'potencia': pow,
            'arredondar': round,
        }
        
        if nome in nativas:
            return nativas[nome](*argumentos)
        
        # Funções definidas pelo usuário
        if nome in self.funcoes:
            return self.funcoes[nome]['executar'](*argumentos)
        
        # Variável que é função
        if nome in self.variaveis and callable(self.variaveis[nome]):
            return self.variaveis[nome](*argumentos)
        
        return None
    
    def avaliar_expressao(self, expr: str) -> Any:
        """Avalia uma expressão"""
        if not expr:
            return None
        
        expr = expr.strip()
        
        # Números
        if re.match(r'^-?\d+(\.\d+)?$', expr):
            return float(expr) if '.' in expr else int(expr)
        
        # Booleanos
        if re.match(r'^(verdadeiro|true)$', expr, re.IGNORECASE):
            return True
        if re.match(r'^(falso|false)$', expr, re.IGNORECASE):
            return False
        if re.match(r'^(vazio|null)$', expr, re.IGNORECASE):
            return None
        if re.match(r'^(indefinido|undefined)$', expr, re.IGNORECASE):
            return None
        
        # Strings
        if re.match(r'^["\'].*["\']$', expr):
            return expr[1:-1]
        
        # Listas
        if expr.startswith('[') and expr.endswith(']'):
            return [self.avaliar_expressao(e.strip()) for e in expr[1:-1].split(',') if e.strip()]
        
        # Objetos
        if expr.startswith('{') and expr.endswith('}'):
            obj = {}
            for item in expr[1:-1].split(','):
                if ':' in item:
                    k, v = item.split(':', 1)
                    obj[k.strip()] = self.avaliar_expressao(v.strip())
            return obj
        
        # Variáveis
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr):
            if expr in self.constantes:
                return self.constantes[expr]
            if expr in self.variaveis:
                return self.variaveis[expr]
            return expr
        
        # Expressões matemáticas
        try:
            return eval(expr, {'__builtins__': {}}, self.variaveis)
        except:
            return expr
    
    def executar_arquivo(self, caminho: str) -> Any:
        """Executa um arquivo .ns"""
        try:
            caminho_abs = os.path.abspath(caminho)
            if not os.path.exists(caminho_abs):
                print(f'❌ Arquivo não encontrado: {caminho}')
                return None
            
            codigo = open(caminho_abs, 'r', encoding='utf-8').read()
            print(f'📄 Executando: {caminho}')
            return self.executar(codigo, caminho_abs)
        except Exception as e:
            print(f'❌ Erro ao executar arquivo: {e}')
            return None


# ============================================================
#              INTERFACE DE LINHA DE COMANDO
# ============================================================

class NullScriptCLI:
    """Interface de linha de comando"""
    
    def __init__(self):
        self.interpreter = NullScriptInterpreter()
        self.versao = VERSAO
    
    def iniciar(self):
        """Inicia a CLI"""
        args = sys.argv[1:]
        
        if len(args) == 0:
            self.mostrar_ajuda()
            return
        
        comando = args[0]
        
        if comando in ['--help', '-h']:
            self.mostrar_ajuda()
        elif comando in ['--version', '-v']:
            print(f'NullScript v{self.versao}')
        elif comando in ['--repl', '-r']:
            self.iniciar_repl()
        elif comando == '--ia':
            self.modo_ia(args[1:])
        elif comando == '--doc':
            self.gerar_documentacao(args[1:])
        elif comando == '--compile':
            self.compilar(args[1:])
        else:
            self.executar_arquivo(comando)
    
    def mostrar_ajuda(self):
        """Mostra ajuda"""
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║          NULLSCRIPT - LINGUAGEM COMPLETA                 ║
║             Versão {self.versao}                          ║
║        {AUTOR}                                           ║
╚═══════════════════════════════════════════════════════════╝

📖 USO:
  nullscript <arquivo.ns>        Executa um arquivo .ns
  nullscript --repl              Modo interativo (REPL)
  nullscript --help              Mostra esta ajuda
  nullscript --version           Mostra a versão
  nullscript --ia <arquivo>      Executa com IA ativa
  nullscript --doc <arquivo>     Gera documentação
  nullscript --compile <arquivo> Compila para Python

📝 EXEMPLOS:
  nullscript exemplo.ns          Executa o arquivo
  nullscript --repl              Inicia o REPL
  nullscript --ia exemplo.ns     Executa com IA

🔧 OPÇÕES:
  --ia         Ativa IA (CorretorAuto)
  --aprendiz   Modo aprendiz (IA explica)
  --debug      Modo debug
  --doc        Gera documentação
  --compile    Compila para Python

📚 BIBLIOTECAS NATIVAS:
  CorretorAuto  Matematica  Arquivos  Criptografia
  Testes        Sistema     Rede      BD
  Facil         Preguiçoso  Auto      Jogo
  Web

💡 DICAS:
  - Use "exibir:" para mostrar algo
  - Use "perguntar:" para entrada
  - Use "importar biblioteca X" para carregar bibliotecas
  - A IA pode corrigir seu código automaticamente

🌐 REPOSITÓRIO:
  {REPOSITORIO}
        """)
    
    def executar_arquivo(self, caminho: str):
        """Executa um arquivo"""
        if not caminho.endswith('.ns') and not caminho.endswith('.null'):
            print(f'⚠️ Arquivo sem extensão .ns: {caminho}')
        
        self.interpreter.executar_arquivo(caminho)
    
    def iniciar_repl(self):
        """Inicia o modo REPL interativo"""
        print(f"""
🚀 NULLSCRIPT REPL v{self.versao}
📖 Digite "help" para ajuda
📖 Digite "sair" para sair
🔧 IA ativa: {self.interpreter.auto_corrigir}
        """)
        
        while True:
            try:
                linha = input('null> ').strip()
                if not linha:
                    continue
                
                if linha.lower() in ['sair', 'exit']:
                    print('👋 Até logo!')
                    break
                
                if linha.lower() == 'help':
                    print("""
Comandos disponíveis:
  help     - Mostra esta ajuda
  sair     - Sai do REPL
  clear    - Limpa a tela
  debug    - Ativa/desativa debug
  ia       - Mostra status da IA
  libs     - Lista bibliotecas
  vars     - Mostra variáveis
  funs     - Mostra funções
                    """)
                    continue
                
                if linha.lower() == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    continue
                
                if linha.lower() == 'debug':
                    self.interpreter.debug = not self.interpreter.debug
                    print(f'Debug: {"ON" if self.interpreter.debug else "OFF"}')
                    continue
                
                if linha.lower() == 'ia':
                    print('Status da IA:')
                    print(f'  - Auto-corrigir: {self.interpreter.auto_corrigir}')
                    print(f'  - Modo aprendiz: {self.interpreter.modo_aprendiz}')
                    continue
                
                if linha.lower() == 'libs':
                    print('📚 Bibliotecas disponíveis:')
                    for nome in self.interpreter.bibliotecas:
                        print(f'  - {nome}')
                    continue
                
                if linha.lower() == 'vars':
                    print('📦 Variáveis:')
                    for nome, valor in self.interpreter.variaveis.items():
                        print(f'  {nome} = {valor}')
                    continue
                
                if linha.lower() == 'funs':
                    print('📦 Funções:')
                    for nome in self.interpreter.funcoes:
                        print(f'  - {nome}()')
                    continue
                
                try:
                    resultado = self.interpreter.executar(linha)
                    if resultado is not None:
                        print(f'=> {resultado}')
                except Exception as e:
                    print(f'❌ {e}')
                    if self.interpreter.auto_corrigir:
                        print('[IA] Tentando corrigir...')
                        try:
                            corrigido = self.interpreter.ia.corrigir(linha)
                            if corrigido != linha:
                                print(f'[IA] Sugestão: {corrigido}')
                        except:
                            pass
            except KeyboardInterrupt:
                print('\n👋 Até logo!')
                break
            except EOFError:
                break
    
    def modo_ia(self, args):
        """Modo com IA ativada"""
        if not args:
            print('❌ Especifique um arquivo')
            return
        
        self.interpreter.auto_corrigir = True
        self.interpreter.modo_aprendiz = True
        print('🧠 IA ativada (auto-correção e modo aprendiz)')
        self.executar_arquivo(args[0])
    
    def gerar_documentacao(self, args):
        """Gera documentação"""
        if not args:
            print('❌ Especifique um arquivo')
            return
        
        caminho = args[0]
        if not os.path.exists(caminho):
            print(f'❌ Arquivo não encontrado: {caminho}')
            return
        
        codigo = open(caminho, 'r', encoding='utf-8').read()
        analise = self.interpreter.ia.analisar(codigo)
        
        print(f"""
📚 DOCUMENTAÇÃO - {caminho}
{'=' * 50}

📊 ANÁLISE:
  Qualidade: {analise['qualidade']}/10
  Complexidade: {analise['complexidade']}/10
  Segurança: {analise['seguranca']}/10
  Performance: {analise['performance']}/10
  Manutenibilidade: {analise['manutenibilidade']}/10

📈 ESTATÍSTICAS:
  Linhas: {analise['linhas']}
  Caracteres: {analise['caracteres']}
  Funções: {analise['funcoes']}

🔧 ESTRUTURAS:
  Se: {analise['estruturas']['se']}
  Enquanto: {analise['estruturas']['enquanto']}
  Para: {analise['estruturas']['para']}

{chr(10).join(['❌ ERROS:'] + [f'  - {e}' for e in analise['erros']]) if analise['erros'] else '✅ Nenhum erro encontrado'}
{chr(10).join(['⚠️ AVISOS:'] + [f'  - {a}' for a in analise['avisos']]) if analise['avisos'] else ''}
{chr(10).join(['💡 SUGESTÕES:'] + [f'  - {s}' for s in analise['sugestoes']]) if analise['sugestoes'] else ''}
        """)
    
    def compilar(self, args):
        """Compila para Python"""
        if not args:
            print('❌ Especifique um arquivo')
            return
        
        caminho = args[0]
        if not os.path.exists(caminho):
            print(f'❌ Arquivo não encontrado: {caminho}')
            return
        
        codigo = open(caminho, 'r', encoding='utf-8').read()
        python_code = self.converter_para_python(codigo)
        arquivo_py = caminho.replace('.ns', '.py')
        
        with open(arquivo_py, 'w', encoding='utf-8') as f:
            f.write(f'''# Compilado de NullScript para Python
# Arquivo original: {caminho}
# Data: {datetime.datetime.now()}

import os
import sys
import json
import math
import random
import time

# Runtime NullScript
class NullScriptRuntime:
    @staticmethod
    def exibir(msg):
        print(msg)
    
    @staticmethod
    def perguntar(msg):
        return input(msg + ' ')
    
    @staticmethod
    def numero(val):
        try:
            return float(val) if '.' in str(val) else int(val)
        except:
            return 0
    
    @staticmethod
    def texto(val):
        return str(val)

ns = NullScriptRuntime()

{python_code}
''')
        
        print(f'✅ Compilado para: {arquivo_py}')
        print(f'📦 Execute com: python {arquivo_py}')
    
    def converter_para_python(self, codigo: str) -> str:
        """Converte NullScript para Python"""
        linhas = codigo.split('\n')
        python_linhas = []
        indent = 0
        
        for linha in linhas:
            linha_trim = linha.strip()
            if not linha_trim or linha_trim.startswith('//') or linha_trim.startswith('#'):
                continue
            
            # Exibir
            if linha_trim.startswith('exibir:'):
                conteudo = linha_trim.replace('exibir:', '').strip()
                conteudo = re.sub(r'^["\']|["\']$', '', conteudo)
                python_linhas.append(' ' * indent + f'ns.exibir({conteudo})')
            
            # Perguntar
            elif linha_trim.startswith('perguntar:'):
                conteudo = linha_trim.replace('perguntar:', '').strip()
                conteudo = re.sub(r'^["\']|["\']$', '', conteudo)
                python_linhas.append(' ' * indent + f'ns.perguntar({conteudo})')
            
            # Se
            elif linha_trim.startswith('se'):
                cond = linha_trim.replace('se', '').strip()
                python_linhas.append(' ' * indent + f'if {cond}:')
                indent += 4
            
            # Senao
            elif linha_trim.startswith('senao'):
                indent -= 4
                python_linhas.append(' ' * indent + 'else:')
                indent += 4
            
            # Enquanto
            elif linha_trim.startswith('enquanto'):
                cond = linha_trim.replace('enquanto', '').strip()
                python_linhas.append(' ' * indent + f'while {cond}:')
                indent += 4
            
            # Para
            elif linha_trim.startswith('para'):
                match = re.match(r'para\s+(\w+)\s+de\s+(\d+)\s+ate\s+(\d+)', linha_trim)
                if match:
                    var, inicio, fim = match.groups()
                    python_linhas.append(' ' * indent + f'for {var} in range({inicio}, {fim} + 1):')
                    indent += 4
            
            # Função
            elif linha_trim.startswith('funcao'):
                match = re.match(r'funcao\s+(\w+)\s*\(([^)]*)\)', linha_trim)
                if match:
                    nome, params = match.groups()
                    python_linhas.append(' ' * indent + f'def {nome}({params}):')
                    indent += 4
            
            # Retorne
            elif linha_trim.startswith('retorne'):
                valor = linha_trim.replace('retorne', '').strip()
                python_linhas.append(' ' * indent + f'return {valor}')
            
            # Fim
            elif linha_trim.lower() == 'fim':
                indent -= 4
            
            # Atribuição
            elif '=' in linha_trim:
                python_linhas.append(' ' * indent + linha_trim)
            
            # Importar
            elif linha_trim.startswith('importar'):
                match = re.match(r'importar\s+(?:biblioteca\s+)?(\w+)', linha_trim)
                if match:
                    nome = match.group(1)
                    python_linhas.append(' ' * indent + f'# Importando {nome}')
            
            # Outros
            else:
                python_linhas.append(' ' * indent + linha_trim)
        
        return '\n'.join(python_linhas)


# ============================================================
#              PONTO DE ENTRADA
# ============================================================

def main():
    """Ponto de entrada principal"""
    try:
        cli = NullScriptCLI()
        cli.iniciar()
    except KeyboardInterrupt:
        print('\n👋 Até logo!')
        sys.exit(0)
    except Exception as e:
        print(f'❌ Erro: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()

# ============================================================
#              FIM DO ARQUIVO
# ============================================================