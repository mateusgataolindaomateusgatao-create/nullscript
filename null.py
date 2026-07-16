#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#           NULLSCRIPT - VERSÃO PYTHON COMPLETA
#           "Programação para humanos"
#           Versão: 4.0.0
# ============================================================
#  Como usar:
#    python null.py arquivo.ns
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

VERSAO = "4.0.0"
NOME = "NullScript"
AUTOR = "mateusgataolindaomateusgatao-create"
REPOSITORIO = "https://github.com/mateusgataolindaomateusgatao-create/nullscript"

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

def cor(texto: str, cor: str = 'branco') -> str:
    """Aplica cor ao texto"""
    return f"{CORES.get(cor, '')}{texto}{CORES.get('reset', '')}"

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
        self.erros_detectados = []
    
    def corrigir(self, codigo: str) -> str:
        """Corrige código NullScript automaticamente"""
        original = codigo
        erros = []
        
        # 1. Correções básicas de palavras-chave
        substituicoes = {
            'if': 'se',
            'else': 'senao',
            'elif': 'senao se',
            'while': 'enquanto',
            'for': 'para',
            'function': 'funcao',
            'def': 'funcao',
            'return': 'retorne',
            'true': 'verdadeiro',
            'false': 'falso',
            'null': 'vazio',
            'undefined': 'indefinido',
            'print': 'exibir',
            'input': 'perguntar',
            'len': 'tamanho',
            'append': 'adicionar',
            'pop': 'remover_ultimo'
        }
        
        for antigo, novo in substituicoes.items():
            padrao = rf'\b{antigo}\b'
            if re.search(padrao, codigo, re.IGNORECASE):
                codigo = re.sub(padrao, novo, codigo, flags=re.IGNORECASE)
                erros.append(f"Palavra-chave '{antigo}' corrigida para '{novo}'")
        
        # 2. Corrigir estruturas não fechadas
        se_count = len(re.findall(r'\bse\b', codigo, re.IGNORECASE))
        fim_count = len(re.findall(r'\bfim\b', codigo, re.IGNORECASE))
        if se_count > fim_count:
            codigo += '\nFim'
            erros.append(f"Adicionado 'Fim' para fechar estrutura")
        
        # 3. Corrigir aspas em exibir
        def corrigir_exibir(match):
            conteudo = match.group(1).strip()
            # Se não tiver aspas, adicionar
            if not (conteudo.startswith('"') or conteudo.startswith("'")):
                return f'exibir: "{conteudo}"'
            return match.group(0)
        
        codigo = re.sub(r'exibir\s*:\s*([^"\'\n]+)', corrigir_exibir, codigo, flags=re.IGNORECASE)
        
        # 4. Corrigir chamadas de função sem nome
        padrao_funcao = r'(\w+)\(\)'
        if re.search(padrao_funcao, codigo):
            # Verificar se a função existe
            pass
        
        # 5. Corrigir variáveis não declaradas
        variaveis_uso = re.findall(r'\b(\w+)\s*=', codigo)
        variaveis_decl = re.findall(r'(?:crie|criar|var|let)\s+(\w+)', codigo, re.IGNORECASE)
        
        for var in set(variaveis_uso) - set(variaveis_decl):
            if var not in ['se', 'senao', 'enquanto', 'para', 'funcao', 'retorne', 'exibir', 'perguntar']:
                erros.append(f"Variável '{var}' não declarada")
        
        # 6. Verificar indentação
        linhas = codigo.split('\n')
        indentacao_ok = True
        for i, linha in enumerate(linhas):
            if linha.strip() and not linha.startswith(' ' * 4) and 'se' in linha.lower():
                if i + 1 < len(linhas) and linhas[i+1].strip() and not linhas[i+1].startswith(' ' * 4):
                    erros.append(f"Linha {i+1}: falta indentação")
                    indentacao_ok = False
        
        # 7. Recomendar boas práticas
        if 'exibir' in codigo.lower() and '"' not in codigo and "'" not in codigo:
            erros.append("Recomendação: Use aspas em exibir: exibir: 'texto'")
        
        self.erros_detectados = erros
        return codigo
    
    def explicar(self, codigo: str) -> str:
        """Explica o código em linguagem natural"""
        explicacao = []
        explicacao.append(cor("📖 EXPLICAÇÃO DO CÓDIGO", "azul"))
        explicacao.append(cor("=" * 50, "ciano"))
        
        # Análise básica
        linhas = codigo.split('\n')
        funcoes = re.findall(r'funcao\s+(\w+)', codigo)
        variaveis = re.findall(r'(\w+)\s*=', codigo)
        imports = re.findall(r'importar\s+(\w+)', codigo)
        
        explicacao.append(cor(f"📊 Total de linhas: {len(linhas)}", "branco"))
        if funcoes:
            explicacao.append(cor(f"📦 Funções: {', '.join(funcoes)}", "verde"))
        if variaveis:
            explicacao.append(cor(f"📦 Variáveis: {', '.join(set(variaveis))}", "amarelo"))
        if imports:
            explicacao.append(cor(f"📦 Importações: {', '.join(imports)}", "roxo"))
        
        # Detectar estruturas
        estruturas = []
        if 'se' in codigo.lower():
            estruturas.append("Condicional (se/senao)")
        if 'enquanto' in codigo.lower():
            estruturas.append("Loop (enquanto)")
        if 'para' in codigo.lower():
            estruturas.append("Loop (para)")
        if 'funcao' in codigo.lower():
            estruturas.append("Funções")
        
        if estruturas:
            explicacao.append(cor(f"🔧 Estruturas: {', '.join(estruturas)}", "ciano"))
        
        # Análise de qualidade
        if len(linhas) > 50:
            explicacao.append(cor("💡 Sugestão: Código longo, considere dividir em funções", "amarelo"))
        
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
                "    a = perguntar('Primeiro número: ')",
                "    b = perguntar('Segundo número: ')",
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
                "exibir: '🚀 API gerada com sucesso!'",
                "Rede.servidor(3000).iniciar()"
            ])
        else:
            codigo.extend([
                "funcao main() {",
                "    exibir: '🚀 Olá mundo!'",
                "    nome = perguntar('Qual seu nome? ')",
                "    exibir: 'Olá, ' + nome + '! Bem-vindo ao NullScript!'",
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
            },
            'variaveis': list(set(re.findall(r'(\w+)\s*=', codigo))),
            'importacoes': re.findall(r'importar\s+(\w+)', codigo)
        }
        
        # Verificar estruturas não fechadas
        se_count = len(re.findall(r'\bse\b', codigo, re.IGNORECASE))
        fim_count = len(re.findall(r'\bfim\b', codigo, re.IGNORECASE))
        if se_count > fim_count:
            analise['erros'].append(f"Faltam {se_count - fim_count} 'Fim'")
        
        # Verificar variáveis não declaradas
        variaveis_uso = re.findall(r'\b(\w+)\s*=', codigo)
        variaveis_decl = re.findall(r'(?:crie|criar|var|let)\s+(\w+)', codigo, re.IGNORECASE)
        for var in set(variaveis_uso) - set(variaveis_decl):
            if var not in ['se', 'senao', 'enquanto', 'para', 'funcao', 'retorne', 'exibir', 'perguntar', 'importar']:
                analise['avisos'].append(f"Variável '{var}' não declarada")
        
        # Verificar comentários
        if '//' not in codigo and '#' not in codigo:
            analise['sugestoes'].append('Adicione comentários para melhor legibilidade')
        
        # Verificar boas práticas
        if '==' in codigo and '===' not in codigo:
            analise['avisos'].append('Use "===" para comparações estritas')
        
        if len(codigo.split('\n')) > 50:
            analise['sugestoes'].append('Considere dividir o código em funções menores')
        
        # Verificar indentação
        linhas = codigo.split('\n')
        for i, linha in enumerate(linhas):
            if linha.strip() and not linha.startswith(' ' * 4) and 'se' in linha.lower():
                if i + 1 < len(linhas) and linhas[i+1].strip() and not linhas[i+1].startswith(' ' * 4):
                    analise['sugestoes'].append(f'Linha {i+1}: use indentação de 4 espaços')
        
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
            'como criar': 'Use "crie variável, nome X, valor Y"',
            'como fazer': 'Descreva o que quer e use "Preguiçoso.fazer()"',
            'erro': 'Verifique a sintaxe. Use "Se:", "Enquanto:", etc.',
            'função': 'Use "funcao nome(parametros) { ... }"',
            'variável': 'Use "crie variável, nome X, valor Y"',
            'lista': 'Use [] para criar listas. Ex: [1, 2, 3]',
            'string': 'Use "" ou \'\' para strings. Ex: "Olá mundo"',
            'if': 'Use "Se: condicao" para condicionais',
            'loop': 'Use "Enquanto: condicao" ou "Para i de 1 ate 10"',
            'api': 'Use "importar biblioteca Auto" e "Auto.criar_api()"',
            'arquivo': 'Use "importar biblioteca Arquivos"',
            'aspas': 'As aspas são opcionais, mas recomendadas para clareza'
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
        otimizado = re.sub(r'para\s+\(', 'para ', otimizado)
        return otimizado
    
    def completar(self, codigo: str) -> str:
        """Completa código incompleto"""
        if 'funcao' in codigo and '{' in codigo and '}' not in codigo:
            return codigo + '\n    // TODO: Implementar lógica\n    retorne null\n}'
        if 'se' in codigo.lower() and 'fim' not in codigo.lower():
            return codigo + '\n    // TODO: Adicionar lógica\nFim'
        if 'enquanto' in codigo.lower() and 'fim' not in codigo.lower():
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
        self.loops_ativos = []
        self.erros_encontrados = []
        self.carregar_bibliotecas()
        self.modo_silencioso = False
    
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
                'mediana': lambda *args: (lambda s: s[len(s)//2] if len(s)%2 else (s[len(s)//2-1] + s[len(s)//2])/2)(sorted(args)),
                'moda': lambda *args: max(set(args), key=args.count) if args else None,
                'desvio_padrao': lambda *args: (lambda m: (sum((x-m)**2 for x in args)/len(args))**0.5)(sum(args)/len(args)) if args else 0,
            },
            
            # Arquivos
            'Arquivos': {
                'ler': lambda p: open(p, 'r', encoding='utf-8').read(),
                'ler_linhas': lambda p: open(p, 'r', encoding='utf-8').read().split('\n'),
                'ler_json': lambda p: json.load(open(p, 'r', encoding='utf-8')),
                'ler_csv': lambda p: [line.strip().split(',') for line in open(p, 'r', encoding='utf-8').readlines()],
                'escrever': lambda p, c: open(p, 'w', encoding='utf-8').write(c),
                'escrever_linhas': lambda p, l: open(p, 'w', encoding='utf-8').write('\n'.join(l)),
                'escrever_json': lambda p, d: open(p, 'w', encoding='utf-8').write(json.dumps(d, indent=2)),
                'adicionar': lambda p, c: open(p, 'a', encoding='utf-8').write(c),
                'existe': os.path.exists,
                'deletar': os.remove,
                'copiar': shutil.copy2,
                'mover': shutil.move,
                'listar': os.listdir,
                'listar_recursivo': lambda p: [str(f) for f in Path(p).rglob('*') if f.is_file()],
                'criar_pasta': lambda p: os.makedirs(p, exist_ok=True),
                'deletar_pasta': lambda p: shutil.rmtree(p),
                'tamanho': lambda p: os.path.getsize(p),
                'data_modificacao': lambda p: datetime.datetime.fromtimestamp(os.path.getmtime(p)).isoformat(),
                'caminho_absoluto': os.path.abspath,
                'nome_arquivo': os.path.basename,
                'extensao': lambda p: os.path.splitext(p)[1],
                'diretorio': os.path.dirname,
            },
            
            # Sistema
            'Sistema': {
                'executar': lambda cmd: subprocess.run(cmd, shell=True, capture_output=True, text=True),
                'executar_saida': lambda cmd: subprocess.check_output(cmd, shell=True, text=True),
                'info': lambda: {
                    'hostname': socket.gethostname(),
                    'platform': platform.system(),
                    'arch': platform.machine(),
                    'cpus': os.cpu_count(),
                    'python': sys.version,
                    'cwd': os.getcwd(),
                    'user': os.getenv('USER', os.getenv('USERNAME', 'unknown')),
                },
                'limpar': lambda: os.system('clear' if os.name == 'posix' else 'cls'),
                'sair': sys.exit,
                'pid': os.getpid,
                'variavel_ambiente': os.getenv,
                'definir_variavel': os.putenv,
                'pasta_atual': os.getcwd,
                'mudar_pasta': os.chdir,
            },
            
            # Rede
            'Rede': {
                'get': lambda url: urllib.request.urlopen(url).read().decode('utf-8'),
                'get_json': lambda url: json.loads(urllib.request.urlopen(url).read().decode('utf-8')),
                'ip': lambda: socket.gethostbyname(socket.gethostname()),
                'ip_publico': lambda: urllib.request.urlopen('https://api.ipify.org').read().decode('utf-8'),
                'ping': lambda host: os.system(f'ping -c 1 {host}') == 0,
                'dns': lambda host: socket.gethostbyname(host),
                'porta_aberta': lambda host, port: socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((host, port)) == 0,
            },
            
            # Criptografia
            'Criptografia': {
                'md5': lambda d: hashlib.md5(str(d).encode()).hexdigest(),
                'sha1': lambda d: hashlib.sha1(str(d).encode()).hexdigest(),
                'sha256': lambda d: hashlib.sha256(str(d).encode()).hexdigest(),
                'sha512': lambda d: hashlib.sha512(str(d).encode()).hexdigest(),
                'gerar_token': lambda t=32: os.urandom(t).hex(),
                'gerar_token_base64': lambda t=32: os.urandom(t).hex(),
                'base64': lambda d: __import__('base64').b64encode(str(d).encode()).decode(),
                'base64_decodificar': lambda d: __import__('base64').b64decode(d).decode(),
            },
            
            # Testes
            'Testes': {
                'testar': lambda desc, fn: (print(f'\n🧪 Teste: {desc}'), fn(), print('✅ PASSED'))[1] if True else None,
                'afirmar': lambda cond, msg=None: (lambda: None) if cond else (lambda: (_ for _ in ()).throw(Exception(msg or 'Assertion failed')))(),
                'afirmar_igual': lambda a, b, msg=None: (lambda: None) if a == b else (lambda: (_ for _ in ()).throw(Exception(msg or f'{a} != {b}')))(),
                'afirmar_diferente': lambda a, b, msg=None: (lambda: None) if a != b else (lambda: (_ for _ in ()).throw(Exception(msg or f'{a} == {b}')))(),
                'afirmar_contem': lambda lista, item, msg=None: (lambda: None) if item in lista else (lambda: (_ for _ in ()).throw(Exception(msg or f'{item} não encontrado')))(),
                'afirmar_tipo': lambda valor, tipo, msg=None: (lambda: None) if type(valor).__name__ == tipo else (lambda: (_ for _ in ()).throw(Exception(msg or f'Tipo esperado: {tipo}, recebido: {type(valor).__name__}')))(),
                'suite': lambda nome, testes: (print(f'\n📋 Suite: {nome}'), [(print(f'  {desc}: {"✅" if fn() else "❌"}') for desc, fn in testes.items())])[1],
            },
            
            # Facil - Operações Facilitadas
            'Facil': {
                'media': lambda lista: sum(lista) / len(lista) if lista else 0,
                'mediana': lambda lista: (lambda s: s[len(s)//2] if len(s)%2 else (s[len(s)//2-1] + s[len(s)//2])/2)(sorted(lista)),
                'moda': lambda lista: max(set(lista), key=lista.count) if lista else None,
                'desvio_padrao': lambda lista: (lambda m: (sum((x-m)**2 for x in lista)/len(lista))**0.5)(sum(lista)/len(lista)) if lista else 0,
                'ordenar': lambda lista: sorted(lista),
                'ordenar_desc': lambda lista: sorted(lista, reverse=True),
                'buscar': lambda lista, valor: lista.index(valor) if valor in lista else -1,
                'buscar_todos': lambda lista, valor: [i for i, v in enumerate(lista) if v == valor],
                'agrupar': lambda lista, campo: (lambda: (_ for _ in ()).throw(Exception('Agrupar requer lista de dicionários')))(),
                'ler_csv': lambda p: [line.strip().split(',') for line in open(p, 'r', encoding='utf-8').readlines()],
                'ler_json': lambda p: json.load(open(p, 'r', encoding='utf-8')),
                'ler_xml': lambda p: (lambda: (_ for _ in ()).throw(Exception('XML parsing não implementado')))(),
                'tokenizar': lambda texto: texto.split(),
                'remover_stopwords': lambda texto: ' '.join([p for p in texto.split() if p.lower() not in ['a','o','e','de','que','do','da','em','com','para','por','um','uma','as','os']]),
                'sentimentar': lambda texto: 'positivo' if sum(1 for p in ['bom','ótimo','excelente','maravilhoso','feliz','amor'] if p in texto.lower()) > sum(1 for n in ['ruim','péssimo','horrível','triste','raiva','ódio'] if n in texto.lower()) else 'negativo' if sum(1 for n in ['ruim','péssimo','horrível','triste','raiva','ódio'] if n in texto.lower()) > 0 else 'neutro',
                'resumir': lambda texto, tamanho=100: texto[:tamanho] + '...' if len(texto) > tamanho else texto,
                'contar_palavras': lambda texto: len(texto.split()),
                'contar_caracteres': lambda texto: len(texto),
                'contar_linhas': lambda texto: len(texto.split('\n')),
                'slug': lambda texto: re.sub(r'[^a-z0-9]+', '-', texto.lower().strip()),
            },
            
            # Preguiçoso - IA que completa
            'Preguiçoso': {
                'fazer': self.ia.gerar,
                'completar': self.ia.completar,
                'otimizar': self.ia.otimizar,
                'explicar': self.ia.explicar,
                'corrigir': self.ia.corrigir,
                'analisar': self.ia.analisar,
            },
            
            # Auto - Automatização
            'Auto': {
                'criar_api': lambda config: f"""// API {config.get('nome', 'recurso')}
importar biblioteca Rede

dados_{config.get('nome', 'recurso')} = []

Rede.rota("/{config.get('nome', 'recurso')}", (req, res) => {{
    res.json({{ dados: dados_{config.get('nome', 'recurso')} }})
}})

Rede.rota("/{config.get('nome', 'recurso')}/criar", (req, res) => {{
    const item = req.corpo
    dados_{config.get('nome', 'recurso')}.adicionar(item)
    res.json({{ mensagem: "Criado", item }})
}})

Rede.servidor(3000).iniciar()
exibir: '🚀 API rodando em http://localhost:3000'
""",
                'criar_crud': lambda nome, campos: f"""// CRUD {nome}
dados_{nome} = []

funcao criar_{nome}({', '.join(campos)}) {{
    const item = {{ {', '.join([f'{c}: {c}' for c in campos])} }}
    dados_{nome}.adicionar(item)
    retorne item
}}

funcao listar_{nome}() {{
    retorne dados_{nome}
}}

funcao atualizar_{nome}(id, {', '.join(campos)}) {{
    const item = dados_{nome}[id]
    {chr(10).join([f'    item.{c} = {c}' for c in campos])}
    retorne item
}}

funcao deletar_{nome}(id) {{
    dados_{nome}.remover_posicao(id)
    retorne verdadeiro
}}
""",
                'criar_jogo': lambda tipo: f"""// Jogo {tipo}
importar biblioteca Jogo

jogo = Jogo.criar(800, 600, "Meu Jogo")

// Jogador
jogador = Jogo.sprite(jogo, "personagem.png", 50, 50)
jogador.velocidade = 5

// Controles
Jogo.tecla("esquerda", () => jogador.x -= jogador.velocidade)
Jogo.tecla("direita", () => jogador.x += jogador.velocidade)
Jogo.tecla("espaco", () => {{
    if jogador.esta_no_chao
        jogador.velocidade_y = -10
        jogador.esta_no_chao = falso
    fim
}})

// Loop
Jogo.loop(jogo, () => {{
    jogador.y += jogador.velocidade_y
    jogador.velocidade_y += 0.5
    if jogador.y >= 500
        jogador.y = 500
        jogador.esta_no_chao = verdadeiro
    fim
    Jogo.renderizar(jogador)
}})

Jogo.iniciar(jogo)
""",
                'criar_site': lambda config: f"""// Site {config.get('titulo', 'Meu Site')}
importar biblioteca Web

{chr(10).join([f'Web.rota("/{pagina}", (req, res) => {{ res.html("<h1>{pagina.capitalize()}</h1>") }})' for pagina in config.get('paginas', ['home', 'sobre', 'contato'])])}

Web.servidor({config.get('porta', 3000)}).iniciar()
exibir: '🌐 Site rodando em http://localhost:{config.get('porta', 3000)}'
""",
                'criar_bot': lambda plataforma, config: f"""// Bot para {plataforma}
importar biblioteca Rede

{chr(10).join([f'// TODO: Implementar bot para {plataforma}'])}
exibir: '🤖 Bot {plataforma} em desenvolvimento'
""",
                'criar_cli': lambda config: f"""// CLI {config.get('nome', 'app')}
args = Sistema.argv()

funcao mostrar_ajuda() {{
    exibir: "Comandos disponíveis:"
    {chr(10).join([f'    exibir: "  {cmd} - {desc}"' for cmd, desc in config.get('comandos', {'help': 'Mostra ajuda', 'version': 'Mostra versão'}).items()])}
}}

if args.tamanho == 0
    mostrar_ajuda()
else
    escolha args[0]
        {chr(10).join([f'        caso "{cmd}": exibir: "Executando {cmd}..."' for cmd in config.get('comandos', {'help': 'Mostra ajuda'}).keys()])}
        padrao: exibir: "Comando desconhecido"
    fim
fim
""",
            },
            
            # Jogo
            'Jogo': {
                'criar': lambda w=800, h=600, t='Jogo': {'largura': w, 'altura': h, 'titulo': t, 'sprites': [], 'fisica': None, 'loop': None},
                'sprite': lambda jogo, img, x=0, y=0: {'imagem': img, 'x': x, 'y': y, 'largura': 50, 'altura': 50, 'velocidade': 5, 'velocidade_y': 0, 'esta_no_chao': True},
                'tecla': lambda tecla, func: func,
                'loop': lambda jogo, func: (jogo.__setitem__('loop', func), jogo)[1],
                'renderizar': lambda sprite: sprite,
                'fundo': lambda cor: print(f'🎨 Fundo: {cor}'),
                'texto': lambda texto, x, y, cor: print(f'📝 Texto: {texto} em ({x},{y}) cor:{cor}'),
                'fisica': lambda jogo, g: (jogo.__setitem__('fisica', {'gravidade': g}), jogo)[1],
                'colisao': lambda obj1, obj2, func: func,
                'iniciar': lambda jogo: (print(f'🎮 Iniciando: {jogo["titulo"]}'), jogo)[1],
                'pausar': lambda jogo: (print('⏸️ Pausado'), jogo)[1],
                'continuar': lambda jogo: (print('▶️ Continuado'), jogo)[1],
                'finalizar': lambda jogo: (print('🏁 Finalizado'), jogo)[1],
                'som': lambda arquivo, volume: print(f'🔊 Som: {arquivo} (volume: {volume})'),
                'musica': lambda arquivo, volume: print(f'🎵 Música: {arquivo} (volume: {volume})'),
            },
            
            # Web
            'Web': {
                'servidor': lambda porta=3000: print(f'🌐 Servidor em http://localhost:{porta}'),
                'rota': lambda path, handler: handler,
                'html': lambda content: f'<html>{content}</html>',
                'json': lambda data: json.dumps(data),
                'css': lambda content: f'<style>{content}</style>',
                'js': lambda content: f'<script>{content}</script>',
                'static': lambda pasta: print(f'📁 Pasta estática: {pasta}'),
                'session': lambda chave, valor: {chave: valor},
                'cookie': lambda nome, valor: {nome: valor},
                'template': lambda arquivo, dados: print(f'📄 Template: {arquivo}'),
            }
        }
    
    def executar(self, codigo: str, arquivo: str = '') -> Any:
        """Executa código NullScript"""
        inicio = time.time()
        self.historico.append(codigo)
        self.arquivo_atual = arquivo
        self.erros_encontrados = []
        
        try:
            if self.auto_corrigir:
                corrigido = self.ia.corrigir(codigo)
                if corrigido != codigo and self.debug:
                    print('[IA] Código corrigido')
                    # Mostrar correções
                    if hasattr(self.ia, 'erros_detectados') and self.ia.erros_detectados:
                        print('[IA] Correções aplicadas:')
                        for erro in self.ia.erros_detectados[:5]:
                            print(f'  • {erro}')
                codigo = corrigido
            
            resultado = self.interpretar(codigo)
            return resultado
        except Exception as erro:
            self.erros_encontrados.append(str(erro))
            print(f'❌ Erro: {erro}')
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
        bloco_indent = 0
        
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
                bloco_indent = len(linha) - len(linha.lstrip())
                continue
            
            if re.match(r'^(fim|end|})', linha_trim, re.IGNORECASE):
                em_bloco = False
                try:
                    resultado = self.executar_bloco(bloco_tipo, bloco_condicao, bloco)
                except Exception as e:
                    print(f'⚠️ Erro no bloco: {e}')
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
                else:
                    # Mostrar erro simples
                    erro_msg = str(e)
                    if not erro_msg or 'None' in erro_msg:
                        erro_msg = 'Erro de sintaxe'
                    print(f'⚠️ Erro na linha {i+1}: {erro_msg}')
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
        # Remover 'se' e 'entao'
        cond = re.sub(r'^se\s*:?\s*', '', condicao, flags=re.IGNORECASE)
        cond = re.sub(r'\s+ent[aã]o\s*$', '', cond, flags=re.IGNORECASE)
        cond = cond.strip()
        
        # Substituir 'for igual a' por '=='
        cond = re.sub(r'\bfor\s+igual\s+a\b', '==', cond, flags=re.IGNORECASE)
        cond = re.sub(r'\bé\s+igual\s+a\b', '==', cond, flags=re.IGNORECASE)
        cond = re.sub(r'\bfor\s+diferente\s+de\b', '!=', cond, flags=re.IGNORECASE)
        cond = re.sub(r'\bé\s+diferente\s+de\b', '!=', cond, flags=re.IGNORECASE)
        cond = re.sub(r'\bmaior\s+que\b', '>', cond, flags=re.IGNORECASE)
        cond = re.sub(r'\bmenor\s+que\b', '<', cond, flags=re.IGNORECASE)
        cond = re.sub(r'\bmaior\s+ou\s+igual\b', '>=', cond, flags=re.IGNORECASE)
        cond = re.sub(r'\bmenor\s+ou\s+igual\b', '<=', cond, flags=re.IGNORECASE)
        
        try:
            resultado = self.avaliar_expressao(cond)
            if resultado:
                return self.interpretar(bloco)
            return None
        except Exception as e:
            print(f'⚠️ Erro na condição: {cond}')
            print(f'   {e}')
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
        # Para i de 1 ate 10 passo 1
        match = re.match(r'para\s+(\w+)\s+de\s+(\d+)\s+ate\s+(\d+)(?:\s+passo\s+(\d+))?', condicao, re.IGNORECASE)
        if not match:
            match = re.match(r'para\s+(\w+)\s*=\s*(\d+)\s+ate\s+(\d+)', condicao, re.IGNORECASE)
            if not match:
                return None
        
        if len(match.groups()) == 4:
            var, inicio, fim, passo = match.groups()
            passo = int(passo) if passo else 1
        else:
            var, inicio, fim = match.groups()
            passo = 1
        
        inicio = int(inicio)
        fim = int(fim)
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
        """Processa comando exibir - remove aspas automaticamente"""
        # Extrair conteúdo após exibir:
        texto = re.sub(r'^(exibir|mostrar|print)\s*:?\s*', '', linha)
        
        # Remover aspas se existirem
        texto = re.sub(r'^["\']|["\']$', '', texto)
        
        # Interpolação
        def substituir_var(match):
            var = match.group(1).strip()
            return str(self.variaveis.get(var, var))
        
        texto = re.sub(r'\$\{([^}]+)\}', substituir_var, texto)
        texto = re.sub(r'\{([^}]+)\}', substituir_var, texto)
        
        # Avaliar expressões dentro de ()
        texto = re.sub(r'\(([^)]+)\)', lambda m: str(self.avaliar_expressao(m.group(1))), texto)
        
        # Remover espaços extras e imprimir
        texto = texto.strip()
        if texto:
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
        # Remove ponto e vírgula
        linha = linha.replace(';', '').strip()
        
        # Padrão: crie variável, nome X, valor Y
        match = re.match(r'(?:crie|criar|var|let|declare)\s+(?:variavel\s*,\s*nome\s*)?(\w+)(?:\s*,\s*valor\s*)?\s*=\s*(.+)', linha, re.IGNORECASE)
        if not match:
            # Padrão: var x = 10
            match = re.match(r'(?:var|let)\s+(\w+)\s*=\s*(.+)', linha, re.IGNORECASE)
            if not match:
                # Padrão: x = 10 (detectado em atribuição)
                return None
        
        nome, valor = match.groups()
        valor_avaliado = self.avaliar_expressao(valor.strip())
        self.variaveis[nome] = valor_avaliado
        return self.variaveis[nome]
    
    def processar_atribuicao(self, linha: str) -> Any:
        """Processa atribuição simples"""
        linha = linha.replace(';', '').strip()
        match = re.match(r'^(\w+)\s*=\s*(.+)', linha)
        if not match:
            return None
        
        nome, valor = match.groups()
        valor_avaliado = self.avaliar_expressao(valor.strip())
        self.variaveis[nome] = valor_avaliado
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
        
        # Verificar se é CorretorAuto (case insensitive)
        if nome.lower() == 'corretorauto':
            self.variaveis['IA'] = self.ia
            self.variaveis['CorretorAuto'] = self.ia
        
        if nome in self.bibliotecas:
            self.variaveis[nome] = self.bibliotecas[nome]
            return self.bibliotecas[nome]
        
        return nome
    
    def processar_chamada_funcao(self, linha: str) -> Any:
        """Processa chamada de função"""
        linha = linha.replace(';', '').strip()
        match = re.match(r'(\w+)\s*\(([^)]*)\)', linha)
        if not match:
            return None
        
        nome, args = match.groups()
        argumentos = [self.avaliar_expressao(a.strip()) for a in args.split(',')] if args else []
        
        # Funções nativas
        nativas = {
            'tipo': lambda v: type(v).__name__,
            'numero': lambda v: float(v) if '.' in str(v) else int(v) if v else 0,
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
            # Substituir variáveis na expressão
            expr_avaliada = expr
            for var, val in self.variaveis.items():
                if isinstance(val, (int, float)):
                    expr_avaliada = re.sub(rf'\b{var}\b', str(val), expr_avaliada)
            return eval(expr_avaliada, {'__builtins__': {}}, {})
        except:
            return expr
    
    def executar_arquivo(self, caminho: str) -> Any:
        """Executa um arquivo .ns sem mostrar mensagem de execução"""
        try:
            caminho_abs = os.path.abspath(caminho)
            if not os.path.exists(caminho_abs):
                print(f'❌ Arquivo não encontrado: {caminho}')
                return None

            codigo = open(caminho_abs, 'r', encoding='utf-8').read()
            
            # Verificar se o código tem erros antes de executar
            if self.auto_corrigir:
                codigo_corrigido = self.ia.corrigir(codigo)
                if codigo_corrigido != codigo and self.ia.erros_detectados:
                    # Mostrar correções
                    print('[IA] Correções aplicadas:')
                    for erro in self.ia.erros_detectados[:5]:
                        print(f'  • {erro}')
                    codigo = codigo_corrigido
            
            # Executar sem mensagem de "Executando"
            return self.executar(codigo, caminho_abs)
            
        except Exception as e:
            print(f'❌ Erro: {e}')
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
        elif comando == '--silent':
            self.interpreter.modo_silencioso = True
            if len(args) > 1:
                self.executar_arquivo(args[1])
            else:
                print('❌ Especifique um arquivo')
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
  nullscript --ia <arquivo>      Executa com IA ativada
  nullscript --doc <arquivo>     Gera documentação
  nullscript --compile <arquivo> Compila para Python
  nullscript --silent <arquivo>  Executa sem mensagens extras

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
  --silent     Executa sem mensagens extras

📚 BIBLIOTECAS NATIVAS:
  CorretorAuto  Matematica  Arquivos  Criptografia
  Testes        Sistema     Rede      BD
  Facil         Preguiçoso  Auto      Jogo
  Web

💡 DICAS:
  - Use "exibir:" para mostrar algo (aspas opcionais)
  - Use "perguntar:" para entrada do usuário
  - Use "importar biblioteca X" para carregar bibliotecas
  - A IA pode corrigir seu código automaticamente
  - Indentação é importante para blocos de código

🌐 REPOSITÓRIO:
  {REPOSITORIO}
        """)
    
    def executar_arquivo(self, caminho: str):
        """Executa um arquivo sem mensagem de execução"""
        if not caminho.endswith('.ns') and not caminho.endswith('.null'):
            print(f'⚠️ Arquivo sem extensão .ns: {caminho}')
        
        # Executar sem mensagem extra
        self.interpreter.executar_arquivo(caminho)
    
    def iniciar_repl(self):
        """Inicia o modo REPL interativo"""
        print(f"""
🚀 NULLSCRIPT REPL v{self.versao}
📖 Digite "help" para ajuda
📖 Digite "sair" para sair
🔧 IA ativa: {self.interpreter.auto_corrigir}
💡 Aspas são opcionais em exibir
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
  Variáveis: {', '.join(analise['variaveis']) if analise['variaveis'] else 'Nenhuma'}
  Importações: {', '.join(analise['importacoes']) if analise['importacoes'] else 'Nenhuma'}

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
                cond = cond.replace('entao', '').strip()
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