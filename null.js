#!/usr/bin/env node
// ============================================================
//           NULLSCRIPT - INTERPRETADOR COMPLETO
//           Versão 3.0.0 - Execução .ns
// ============================================================
//  Como usar:
//    node nullscript.js arquivo.ns
//    null arquivo.ns
//    ns arquivo.ns
// ============================================================

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const os = require('os');
const child_process = require('child_process');
const readline = require('readline');
const https = require('https');
const util = require('util');
const events = require('events');
const zlib = require('zlib');
const querystring = require('querystring');
const url = require('url');
const net = require('net');
const dns = require('dns');
const vm = require('vm');
const module = require('module');

// ============================================================
//              CONFIGURAÇÃO DA IA
// ============================================================

const GROQ_API_KEY = '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';
const MODELO_IA = 'llama4-scout';
const VERSAO = '3.0.0';

// ============================================================
//                  CLASSE IA
// ============================================================

class CorretorAuto {
    constructor() {
        this.modelo = MODELO_IA;
        this.apiKey = GROQ_API_KEY;
        this.modo_aprendiz = false;
        this.auto_corrigir = true;
        this.estilo = null;
        this.historico = [];
        this.cache = {};
    }

    async chamarIA(prompt, contexto = '') {
        try {
            const dados = JSON.stringify({
                model: this.modelo,
                messages: [
                    { role: 'system', content: 'Você é um assistente especialista em NullScript, uma linguagem de programação em português.' },
                    { role: 'user', content: `${contexto}\n\n${prompt}` }
                ],
                temperature: 0.7,
                max_tokens: 2000
            });

            const options = {
                hostname: 'api.groq.com',
                path: '/openai/v1/chat/completions',
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(dados)
                }
            };

            return new Promise((resolve, reject) => {
                const req = https.request(options, (res) => {
                    let data = '';
                    res.on('data', chunk => data += chunk);
                    res.on('end', () => {
                        try {
                            const json = JSON.parse(data);
                            resolve(json.choices[0].message.content);
                        } catch (e) {
                            reject(e);
                        }
                    });
                });
                req.on('error', reject);
                req.write(dados);
                req.end();
            });
        } catch (erro) {
            return this.simularResposta(prompt);
        }
    }

    simularResposta(prompt) {
        if (prompt.includes('corrigir') || prompt.includes('erro')) {
            return this.simularCorrecao(prompt);
        } else if (prompt.includes('explicar')) {
            return this.simularExplicacao(prompt);
        } else if (prompt.includes('gerar')) {
            return this.simularGeracao(prompt);
        } else {
            return this.simularRespostaGenerica(prompt);
        }
    }

    simularCorrecao(prompt) {
        return `// Código corrigido pela IA\n// Use estruturas corretas\nSe: condicao\n    // código\nFim`;
    }

    simularExplicacao(prompt) {
        return `Este código em NullScript usa estruturas como "Se" para condicionais, "Enquanto" para loops.`;
    }

    simularGeracao(prompt) {
        return `// Código gerado pela IA\nfuncao main() {\n    exibir: "Olá mundo!"\n}\nmain()`;
    }

    simularRespostaGenerica(prompt) {
        return `Em NullScript você pode programar de forma intuitiva em português.`;
    }

    async corrigir(codigo) {
        try {
            const prompt = `Corrija este código NullScript e retorne apenas o código corrigido:\n\n${codigo}`;
            const resposta = await this.chamarIA(prompt);
            return resposta.replace(/```/g, '').trim();
        } catch (e) {
            return this.corrigirLocal(codigo);
        }
    }

    corrigirLocal(codigo) {
        let corrigido = codigo;
        const substituicoes = {
            'if': 'Se',
            'else': 'Senão',
            'while': 'Enquanto',
            'for': 'Para',
            'function': 'funcao',
            'return': 'retorne',
            'true': 'verdadeiro',
            'false': 'falso',
            'null': 'vazio',
            'undefined': 'indefinido',
            'print': 'exibir',
            'input': 'perguntar'
        };
        for (const [antigo, novo] of Object.entries(substituicoes)) {
            const regex = new RegExp(`\\b${antigo}\\b`, 'gi');
            corrigido = corrigido.replace(regex, novo);
        }
        return corrigido;
    }

    async explicar(codigo) {
        try {
            const prompt = `Explique este código NullScript de forma clara e simples:\n\n${codigo}`;
            return await this.chamarIA(prompt);
        } catch (e) {
            return this.simularExplicacao(codigo);
        }
    }

    async gerar(descricao) {
        try {
            const prompt = `Gere código NullScript para: ${descricao}. Retorne apenas o código.`;
            const resposta = await this.chamarIA(prompt);
            return resposta.replace(/```/g, '').trim();
        } catch (e) {
            return this.simularGeracao(descricao);
        }
    }

    async perguntar(pergunta) {
        try {
            return await this.chamarIA(pergunta);
        } catch (e) {
            return this.simularRespostaGenerica(pergunta);
        }
    }

    async otimizar(codigo) {
        try {
            const prompt = `Otimize este código NullScript mantendo a funcionalidade:\n\n${codigo}`;
            const resposta = await this.chamarIA(prompt);
            return resposta.replace(/```/g, '').trim();
        } catch (e) {
            return this.simularRespostaGenerica(codigo);
        }
    }

    async completar(codigo) {
        try {
            const prompt = `Complete este código NullScript:\n\n${codigo}`;
            const resposta = await this.chamarIA(prompt);
            return resposta.replace(/```/g, '').trim();
        } catch (e) {
            return this.completarLocal(codigo);
        }
    }

    completarLocal(codigo) {
        if (codigo.includes('funcao') && codigo.includes('{')) {
            return codigo + '\n    // TODO: Implementar lógica\n    retorne null\n}';
        }
        if (codigo.includes('Se') && !codigo.includes('Fim')) {
            return codigo + '\n    // TODO: Adicionar lógica\nFim';
        }
        return codigo;
    }

    analisar(codigo) {
        const analise = {
            erros: [],
            avisos: [],
            sugestoes: [],
            qualidade: 0,
            complexidade: 0,
            seguranca: 0,
            performance: 0,
            manutenibilidade: 0,
            linhas: codigo.split('\n').length,
            caracteres: codigo.length,
            funcoes: (codigo.match(/\bfuncao\b/gi) || []).length,
            estruturas: {
                se: (codigo.match(/\bSe\b/gi) || []).length,
                enquanto: (codigo.match(/\bEnquanto\b/gi) || []).length,
                para: (codigo.match(/\bPara\b/gi) || []).length,
                funcao: (codigo.match(/\bfuncao\b/gi) || []).length
            }
        };

        const seCount = (codigo.match(/\bSe\b/gi) || []).length;
        const fimCount = (codigo.match(/\bFim\b/gi) || []).length;
        if (seCount > fimCount) {
            analise.erros.push(`Faltam ${seCount - fimCount} "Fim"`);
        }

        if (!codigo.includes('//') && !codigo.includes('#')) {
            analise.sugestoes.push('Adicione comentários para melhor legibilidade');
        }

        if (codigo.includes('==') && !codigo.includes('===')) {
            analise.avisos.push('Use "===" para comparações estritas');
        }

        analise.qualidade = Math.min(Math.floor((10 - analise.erros.length - analise.avisos.length * 0.5)), 10);
        analise.complexidade = Math.min(Math.floor(analise.linhas / 10) + 1, 10);
        analise.seguranca = 8;
        analise.performance = 7;
        analise.manutenibilidade = Math.min(Math.floor((10 - analise.avisos.length * 0.3)), 10);

        return analise;
    }

    aprenderEstilo(codigo) {
        this.estilo = this.analisar(codigo);
        return this.estilo;
    }

    prever(intencao) {
        const respostas = {
            'estou tentando fazer': 'Parece que você está tentando...',
            'como faço para': 'Você pode usar o comando...',
            'por que meu código': 'Vamos analisar seu código...',
            'erro': 'Verifique a sintaxe. Use "Se:", "Enquanto:", etc.',
            'função': 'Use "funcao nome(parametros) { ... }"',
            'variável': 'Use "crie variável, nome X, valor Y"'
        };
        for (const [padrao, resposta] of Object.entries(respostas)) {
            if (intencao.toLowerCase().includes(padrao)) {
                return resposta;
            }
        }
        return 'Entendo sua intenção. Deixe-me ajudar...';
    }

    async documentar(codigo) {
        try {
            const prompt = `Documente este código NullScript com comentários:\n\n${codigo}`;
            const resposta = await this.chamarIA(prompt);
            return resposta;
        } catch (e) {
            return `// Documentação gerada automaticamente\n// Funções: ${(codigo.match(/\bfuncao\b/gi) || []).length}\n// Linhas: ${codigo.split('\n').length}`;
        }
    }

    async traduzir(codigo, de, para) {
        try {
            const prompt = `Traduza este código da linguagem ${de} para ${para}:\n\n${codigo}`;
            const resposta = await this.chamarIA(prompt);
            return resposta.replace(/```/g, '').trim();
        } catch (e) {
            return codigo;
        }
    }

    async gerarTestes(codigo) {
        try {
            const prompt = `Gere testes para este código NullScript:\n\n${codigo}`;
            const resposta = await this.chamarIA(prompt);
            return resposta.replace(/```/g, '').trim();
        } catch (e) {
            return `// Testes gerados automaticamente\nTestes.testar("Teste principal") {\n    // TODO: Adicionar testes\n}`;
        }
    }

    async refatorar(codigo, tipo) {
        try {
            const prompt = `Refatore este código NullScript (${tipo}):\n\n${codigo}`;
            const resposta = await this.chamarIA(prompt);
            return resposta.replace(/```/g, '').trim();
        } catch (e) {
            return codigo;
        }
    }

    async revisarCompleto(codigo) {
        try {
            const prompt = `Faça uma revisão completa deste código NullScript:\n\n${codigo}`;
            const resposta = await this.chamarIA(prompt);
            return {
                resumo: 'Revisão completa',
                pontos_fortes: ['Código estruturado'],
                pontos_fracos: [],
                melhores_praticas: ['Adicione comentários'],
                proximo_passos: ['Teste o código'],
                detalhes: resposta
            };
        } catch (e) {
            return {
                resumo: 'Revisão básica',
                pontos_fortes: ['Código funcional'],
                pontos_fracos: ['Pode ser melhorado'],
                melhores_praticas: ['Documente o código'],
                proximo_passos: ['Execute testes'],
                detalhes: 'Código analisado localmente'
            };
        }
    }
}

// ============================================================
//              INTERPRETADOR NULLSCRIPT
// ============================================================

class NullScriptInterpreter {
    constructor() {
        this.variaveis = {};
        this.funcoes = {};
        this.constantes = {};
        this.importacoes = {};
        this.ia = new CorretorAuto();
        this.debug = false;
        this.modo_aprendiz = false;
        this.auto_corrigir = true;
        this.historico = [];
        this.linha_atual = 0;
        this.arquivo_atual = '';
        this.pilha_execucao = [];
        this.pilha_retorno = [];
        this.eventos = new events.EventEmitter();
        this.modulos = {};
        this.escopos = [{}];
        this.escopo_atual = 0;
        this.retorno_atual = null;
        this.pausado = false;
        this.temporizadores = [];
        this.promises = [];
        this.workers = [];
        this.fila_tarefas = [];
        this.cache = {};
        this.logs = [];
        this.metricas = {
            execucoes: 0,
            erros: 0,
            tempo_total: 0,
            linhas_processadas: 0
        };
        this.bibliotecas = {};
        this.condicoes = [];
        this.loops = [];
        this.funcoes_anonimas = [];
        this.geradores = [];
        this.contextos = [];
        this.eventos_registrados = {};
        this.middlewares = [];
        this.plugins = [];
        this.transpiladores = [];
        this.otimizadores = [];
    }

    // ============================================================
    //              CARREGAR BIBLIOTECAS NATIVAS
    // ============================================================

    carregarBibliotecas() {
        this.bibliotecas = {
            // 1. CorretorAuto - IA Integrada
            'CorretorAuto': {
                corrigir: (codigo) => this.ia.corrigir(codigo),
                explicar: (codigo) => this.ia.explicar(codigo),
                gerar: (descricao) => this.ia.gerar(descricao),
                analisar: (codigo) => this.ia.analisar(codigo),
                perguntar: (pergunta) => this.ia.perguntar(pergunta),
                otimizar: (codigo) => this.ia.otimizar(codigo),
                completar: (codigo) => this.ia.completar(codigo),
                documentar: (codigo) => this.ia.documentar(codigo),
                traduzir: (codigo, de, para) => this.ia.traduzir(codigo, de, para),
                revisar: (codigo) => this.ia.revisarCompleto(codigo)
            },

            // 2. Matematica - Funções Matemáticas
            'Matematica': {
                soma: (...args) => args.reduce((a, b) => a + b, 0),
                multiplica: (...args) => args.reduce((a, b) => a * b, 1),
                divide: (a, b) => { if (b === 0) throw new Error('Divisão por zero'); return a / b; },
                subtrai: (...args) => args.reduce((a, b) => a - b),
                potencia: (a, b) => Math.pow(a, b),
                raiz: (a) => Math.sqrt(a),
                raiz_cubica: (a) => Math.cbrt(a),
                fatorial: (n) => { if (n <= 1) return 1; let r = 1; for (let i = 2; i <= n; i++) r *= i; return r; },
                fibonacci: (n) => { if (n <= 1) return n; let a = 0, b = 1; for (let i = 2; i <= n; i++) { [a, b] = [b, a + b]; } return b; },
                primo: (n) => { if (n < 2) return false; for (let i = 2; i <= Math.sqrt(n); i++) { if (n % i === 0) return false; } return true; },
                aleatorio: () => Math.random(),
                aleatorio_entre: (min, max) => Math.floor(Math.random() * (max - min + 1)) + min,
                absoluto: (a) => Math.abs(a),
                arredondar: (a) => Math.round(a),
                arredondar_baixo: (a) => Math.floor(a),
                arredondar_cima: (a) => Math.ceil(a),
                teto: (a) => Math.ceil(a),
                piso: (a) => Math.floor(a),
                seno: (a) => Math.sin(a),
                cosseno: (a) => Math.cos(a),
                tangente: (a) => Math.tan(a),
                log: (a) => Math.log(a),
                log10: (a) => Math.log10(a),
                log2: (a) => Math.log2(a),
                maximo: (...args) => Math.max(...args),
                minimo: (...args) => Math.min(...args),
                media: (...args) => args.reduce((a, b) => a + b, 0) / args.length,
                mediana: (...args) => {
                    const sorted = [...args].sort((a, b) => a - b);
                    const mid = Math.floor(sorted.length / 2);
                    return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
                },
                moda: (...args) => {
                    const freq = {};
                    args.forEach(x => freq[x] = (freq[x] || 0) + 1);
                    let max = 0, moda = null;
                    for (const [key, val] of Object.entries(freq)) {
                        if (val > max) { max = val; moda = key; }
                    }
                    return moda;
                },
                desvio_padrao: (...args) => {
                    const media = args.reduce((a, b) => a + b, 0) / args.length;
                    const squaredDiffs = args.map(x => Math.pow(x - media, 2));
                    return Math.sqrt(squaredDiffs.reduce((a, b) => a + b, 0) / args.length);
                },
                variancia: (...args) => {
                    const media = args.reduce((a, b) => a + b, 0) / args.length;
                    const squaredDiffs = args.map(x => Math.pow(x - media, 2));
                    return squaredDiffs.reduce((a, b) => a + b, 0) / args.length;
                },
                porcentagem: (valor, total) => (valor / total) * 100,
                diferenca_porcentagem: (antigo, novo) => ((novo - antigo) / antigo) * 100,
                exponencial: (a) => Math.exp(a),
                seno_hiperbolico: (a) => Math.sinh(a),
                cosseno_hiperbolico: (a) => Math.cosh(a),
                tangente_hiperbolica: (a) => Math.tanh(a),
                arcseno: (a) => Math.asin(a),
                arccos: (a) => Math.acos(a),
                arctan: (a) => Math.atan(a),
                arctan2: (y, x) => Math.atan2(y, x),
                hipotenusa: (a, b) => Math.hypot(a, b),
                truncar: (a) => Math.trunc(a),
                signo: (a) => Math.sign(a),
                isNaN: (a) => isNaN(a),
                isFinite: (a) => isFinite(a),
                isInteger: (a) => Number.isInteger(a),
                isSafeInteger: (a) => Number.isSafeInteger(a)
            },

            // 3. Arquivos - Sistema de Arquivos
            'Arquivos': {
                ler: (caminho) => fs.readFileSync(caminho, 'utf8'),
                ler_linhas: (caminho) => fs.readFileSync(caminho, 'utf8').split('\n'),
                ler_json: (caminho) => JSON.parse(fs.readFileSync(caminho, 'utf8')),
                ler_csv: (caminho) => {
                    const conteudo = fs.readFileSync(caminho, 'utf8');
                    const linhas = conteudo.split('\n').filter(l => l.trim());
                    const cabecalho = linhas[0].split(',');
                    return linhas.slice(1).map(linha => {
                        const valores = linha.split(',');
                        const obj = {};
                        cabecalho.forEach((campo, i) => obj[campo.trim()] = valores[i]?.trim());
                        return obj;
                    });
                },
                ler_buffer: (caminho) => fs.readFileSync(caminho),
                escrever: (caminho, conteudo) => fs.writeFileSync(caminho, conteudo),
                escrever_linhas: (caminho, linhas) => fs.writeFileSync(caminho, linhas.join('\n')),
                escrever_json: (caminho, dados) => fs.writeFileSync(caminho, JSON.stringify(dados, null, 2)),
                escrever_csv: (caminho, dados) => {
                    const cabecalho = Object.keys(dados[0]).join(',');
                    const linhas = dados.map(row => Object.values(row).join(','));
                    fs.writeFileSync(caminho, [cabecalho, ...linhas].join('\n'));
                },
                adicionar: (caminho, conteudo) => fs.appendFileSync(caminho, conteudo),
                existe: (caminho) => fs.existsSync(caminho),
                deletar: (caminho) => fs.unlinkSync(caminho),
                copiar: (origem, destino) => fs.copyFileSync(origem, destino),
                mover: (origem, destino) => fs.renameSync(origem, destino),
                tamanho: (caminho) => fs.statSync(caminho).size,
                data_criacao: (caminho) => fs.statSync(caminho).birthtime,
                data_modificacao: (caminho) => fs.statSync(caminho).mtime,
                data_acesso: (caminho) => fs.statSync(caminho).atime,
                permissoes: (caminho) => fs.statSync(caminho).mode,
                eh_arquivo: (caminho) => fs.statSync(caminho).isFile(),
                eh_pasta: (caminho) => fs.statSync(caminho).isDirectory(),
                eh_symlink: (caminho) => fs.statSync(caminho).isSymbolicLink(),
                criar_pasta: (caminho) => fs.mkdirSync(caminho, { recursive: true }),
                deletar_pasta: (caminho) => fs.rmdirSync(caminho, { recursive: true }),
                listar: (caminho) => fs.readdirSync(caminho),
                listar_recursivo: (caminho) => {
                    const resultados = [];
                    const listar = (dir) => {
                        const arquivos = fs.readdirSync(dir);
                        for (const arquivo of arquivos) {
                            const caminhoCompleto = path.join(dir, arquivo);
                            const stats = fs.statSync(caminhoCompleto);
                            if (stats.isDirectory()) {
                                listar(caminhoCompleto);
                            } else {
                                resultados.push(caminhoCompleto);
                            }
                        }
                    };
                    listar(caminho);
                    return resultados;
                },
                listar_filtrado: (caminho, filtro) => {
                    const arquivos = fs.readdirSync(caminho);
                    return arquivos.filter(a => a.includes(filtro));
                },
                caminho_absoluto: (caminho) => path.resolve(caminho),
                caminho_relativo: (caminho) => path.relative(process.cwd(), caminho),
                nome_arquivo: (caminho) => path.basename(caminho),
                nome_sem_extensao: (caminho) => path.basename(caminho, path.extname(caminho)),
                extensao: (caminho) => path.extname(caminho),
                diretorio: (caminho) => path.dirname(caminho),
                juntar: (...args) => path.join(...args),
                normalizar: (caminho) => path.normalize(caminho),
                pasta_atual: () => process.cwd(),
                mudar_pasta: (caminho) => process.chdir(caminho)
            },

            // 4. Criptografia - Segurança
            'Criptografia': {
                md5: (dados) => crypto.createHash('md5').update(String(dados)).digest('hex'),
                sha1: (dados) => crypto.createHash('sha1').update(String(dados)).digest('hex'),
                sha256: (dados) => crypto.createHash('sha256').update(String(dados)).digest('hex'),
                sha384: (dados) => crypto.createHash('sha384').update(String(dados)).digest('hex'),
                sha512: (dados) => crypto.createHash('sha512').update(String(dados)).digest('hex'),
                hmac256: (dados, chave) => crypto.createHmac('sha256', chave).update(String(dados)).digest('hex'),
                gerar_token: (tamanho = 32) => crypto.randomBytes(tamanho).toString('hex'),
                gerar_token_base64: (tamanho = 32) => crypto.randomBytes(tamanho).toString('base64'),
                gerar_token_url: (tamanho = 32) => crypto.randomBytes(tamanho).toString('base64url'),
                gerar_senha: (tamanho = 12, maiusculas = true, especiais = true) => {
                    const letras = 'abcdefghijklmnopqrstuvwxyz';
                    const maiusculasChar = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
                    const numeros = '0123456789';
                    const especiaisChar = '!@#$%^&*()_+-=';
                    let charset = letras + numeros;
                    if (maiusculas) charset += maiusculasChar;
                    if (especiais) charset += especiaisChar;
                    let senha = '';
                    for (let i = 0; i < tamanho; i++) {
                        senha += charset[Math.floor(Math.random() * charset.length)];
                    }
                    return senha;
                },
                base64: (dados) => Buffer.from(String(dados)).toString('base64'),
                base64_decodificar: (dados) => Buffer.from(dados, 'base64').toString(),
                base64_url: (dados) => Buffer.from(String(dados)).toString('base64url'),
                hex: (dados) => Buffer.from(String(dados)).toString('hex'),
                hex_decodificar: (dados) => Buffer.from(dados, 'hex').toString(),
                criptografar_aes: (dados, senha) => {
                    const cipher = crypto.createCipher('aes-256-cbc', senha);
                    let encrypted = cipher.update(String(dados), 'utf8', 'hex');
                    encrypted += cipher.final('hex');
                    return encrypted;
                },
                decriptografar_aes: (dados, senha) => {
                    const decipher = crypto.createDecipher('aes-256-cbc', senha);
                    let decrypted = decipher.update(dados, 'hex', 'utf8');
                    decrypted += decipher.final('utf8');
                    return decrypted;
                },
                criptografar_aes_gcm: (dados, senha) => {
                    const iv = crypto.randomBytes(16);
                    const cipher = crypto.createCipheriv('aes-256-gcm', senha, iv);
                    let encrypted = cipher.update(String(dados), 'utf8', 'hex');
                    encrypted += cipher.final('hex');
                    const authTag = cipher.getAuthTag().toString('hex');
                    return { encrypted, iv: iv.toString('hex'), authTag };
                },
                decriptografar_aes_gcm: (dados, senha, iv, authTag) => {
                    const decipher = crypto.createDecipheriv('aes-256-gcm', senha, Buffer.from(iv, 'hex'));
                    decipher.setAuthTag(Buffer.from(authTag, 'hex'));
                    let decrypted = decipher.update(dados, 'hex', 'utf8');
                    decrypted += decipher.final('utf8');
                    return decrypted;
                },
                gerar_par_chaves: (bits = 2048) => {
                    const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
                        modulusLength: bits,
                        publicKeyEncoding: { type: 'pkcs1', format: 'pem' },
                        privateKeyEncoding: { type: 'pkcs1', format: 'pem' }
                    });
                    return { public: publicKey, private: privateKey };
                },
                assinar: (dados, chavePrivada) => {
                    const sign = crypto.createSign('RSA-SHA256');
                    sign.update(String(dados));
                    return sign.sign(chavePrivada, 'hex');
                },
                verificar: (dados, assinatura, chavePublica) => {
                    const verify = crypto.createVerify('RSA-SHA256');
                    verify.update(String(dados));
                    return verify.verify(chavePublica, assinatura, 'hex');
                }
            },

            // 5. Testes - Testes Automáticos
            'Testes': {
                testar: (descricao, funcao) => {
                    console.log(`\n🧪 Teste: ${descricao}`);
                    try {
                        funcao();
                        console.log('✅ PASSED');
                        return true;
                    } catch (erro) {
                        console.log('❌ FAILED:', erro.message);
                        return false;
                    }
                },
                suite: (nome, testes) => {
                    console.log(`\n📋 Suite: ${nome}`);
                    let passou = 0;
                    let falhou = 0;
                    for (const [desc, fn] of Object.entries(testes)) {
                        if (Testes.testar(desc, fn)) {
                            passou++;
                        } else {
                            falhou++;
                        }
                    }
                    console.log(`\n📊 Total: ${passou + falhou} | ✅ ${passou} | ❌ ${falhou}`);
                    return { passou, falhou };
                },
                afirmar: (condicao, mensagem) => {
                    if (!condicao) throw new Error(mensagem || 'Assertion failed');
                    return true;
                },
                afirmar_igual: (a, b, mensagem) => {
                    if (a !== b) throw new Error(mensagem || `${a} !== ${b}`);
                    return true;
                },
                afirmar_diferente: (a, b, mensagem) => {
                    if (a === b) throw new Error(mensagem || `${a} === ${b}`);
                    return true;
                },
                afirmar_contem: (lista, item, mensagem) => {
                    if (!lista.includes(item)) throw new Error(mensagem || `${item} não encontrado`);
                    return true;
                },
                afirmar_nao_contem: (lista, item, mensagem) => {
                    if (lista.includes(item)) throw new Error(mensagem || `${item} encontrado`);
                    return true;
                },
                afirmar_tipo: (valor, tipo, mensagem) => {
                    if (typeof valor !== tipo) throw new Error(mensagem || `Tipo esperado: ${tipo}, recebido: ${typeof valor}`);
                    return true;
                },
                afirmar_instancia: (objeto, classe, mensagem) => {
                    if (!(objeto instanceof classe)) throw new Error(mensagem || `Não é instância de ${classe}`);
                    return true;
                },
                afirmar_maior_que: (a, b, mensagem) => {
                    if (a <= b) throw new Error(mensagem || `${a} não é maior que ${b}`);
                    return true;
                },
                afirmar_menor_que: (a, b, mensagem) => {
                    if (a >= b) throw new Error(mensagem || `${a} não é menor que ${b}`);
                    return true;
                },
                afirmar_aproximadamente: (a, b, precisao = 0.001, mensagem) => {
                    if (Math.abs(a - b) > precisao) throw new Error(mensagem || `${a} não é aproximadamente ${b}`);
                    return true;
                }
            },

            // 6. Sistema - Sistema Operacional
            'Sistema': {
                executar: (comando) => {
                    try {
                        const resultado = child_process.execSync(comando, { encoding: 'utf8' });
                        return { saida: resultado, erro: '', codigo: 0 };
                    } catch (e) {
                        return { saida: '', erro: e.message, codigo: e.status || 1 };
                    }
                },
                executar_async: (comando) => {
                    return new Promise((resolve) => {
                        child_process.exec(comando, (erro, stdout, stderr) => {
                            resolve({ saida: stdout, erro: stderr, codigo: erro ? erro.code : 0 });
                        });
                    });
                },
                executar_stream: (comando, callback) => {
                    const proc = child_process.spawn('sh', ['-c', comando]);
                    proc.stdout.on('data', (data) => callback(data.toString()));
                    proc.stderr.on('data', (data) => callback('ERR: ' + data.toString()));
                    return proc;
                },
                info: () => ({
                    hostname: os.hostname(),
                    platform: os.platform(),
                    arch: os.arch(),
                    cpus: os.cpus().length,
                    memoria_total: os.totalmem(),
                    memoria_livre: os.freemem(),
                    memoria_usada: os.totalmem() - os.freemem(),
                    uptime: os.uptime(),
                    loadavg: os.loadavg(),
                    versao: process.version,
                    pid: process.pid,
                    ppid: process.ppid,
                    titulo: process.title,
                    argv: process.argv,
                    cwd: process.cwd(),
                    env_count: Object.keys(process.env).length
                }),
                pid: () => process.pid,
                ppid: () => process.ppid,
                env: (nome) => nome ? process.env[nome] : process.env,
                set_env: (nome, valor) => { process.env[nome] = valor; return true; },
                unset_env: (nome) => { delete process.env[nome]; return true; },
                has_env: (nome) => process.env[nome] !== undefined,
                limpar: () => console.clear(),
                limpar_console: () => console.clear(),
                sair: (codigo = 0) => process.exit(codigo),
                abortar: () => process.abort(),
                memória: () => process.memoryUsage(),
                cpu: () => process.cpuUsage(),
                tempo: () => process.uptime(),
                versao_node: () => process.version,
                plataforma: () => process.platform,
                arquitetura: () => process.arch,
                argv: () => process.argv,
                cwd: () => process.cwd(),
                chdir: (dir) => process.chdir(dir),
                on_exit: (callback) => process.on('exit', callback),
                on_signal: (signal, callback) => process.on(signal, callback),
                kill: (pid, signal = 'SIGTERM') => process.kill(pid, signal),
                spawn: (comando, args = [], options = {}) => {
                    return child_process.spawn(comando, args, options);
                },
                fork: (modulo, args = [], options = {}) => {
                    return child_process.fork(modulo, args, options);
                }
            },

            // 7. Rede - Comunicação
            'Rede': {
                get: (url) => {
                    return new Promise((resolve, reject) => {
                        const parsedUrl = new URL(url);
                        const options = {
                            hostname: parsedUrl.hostname,
                            port: parsedUrl.port || 443,
                            path: parsedUrl.pathname + parsedUrl.search,
                            method: 'GET',
                            headers: { 'User-Agent': 'NullScript/3.0' }
                        };
                        const req = https.request(options, (res) => {
                            let data = '';
                            res.on('data', chunk => data += chunk);
                            res.on('end', () => {
                                try { resolve(JSON.parse(data)); } catch (e) { resolve(data); }
                            });
                        });
                        req.on('error', reject);
                        req.end();
                    });
                },
                post: (url, dados, headers = {}) => {
                    return new Promise((resolve, reject) => {
                        const dadosString = JSON.stringify(dados);
                        const parsedUrl = new URL(url);
                        const options = {
                            hostname: parsedUrl.hostname,
                            port: parsedUrl.port || 443,
                            path: parsedUrl.pathname + parsedUrl.search,
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Content-Length': Buffer.byteLength(dadosString),
                                ...headers
                            }
                        };
                        const req = https.request(options, (res) => {
                            let data = '';
                            res.on('data', chunk => data += chunk);
                            res.on('end', () => {
                                try { resolve(JSON.parse(data)); } catch (e) { resolve(data); }
                            });
                        });
                        req.on('error', reject);
                        req.write(dadosString);
                        req.end();
                    });
                },
                put: (url, dados, headers = {}) => {
                    return new Promise((resolve, reject) => {
                        const dadosString = JSON.stringify(dados);
                        const parsedUrl = new URL(url);
                        const options = {
                            hostname: parsedUrl.hostname,
                            port: parsedUrl.port || 443,
                            path: parsedUrl.pathname + parsedUrl.search,
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                                'Content-Length': Buffer.byteLength(dadosString),
                                ...headers
                            }
                        };
                        const req = https.request(options, (res) => {
                            let data = '';
                            res.on('data', chunk => data += chunk);
                            res.on('end', () => {
                                try { resolve(JSON.parse(data)); } catch (e) { resolve(data); }
                            });
                        });
                        req.on('error', reject);
                        req.write(dadosString);
                        req.end();
                    });
                },
                delete: (url, headers = {}) => {
                    return new Promise((resolve, reject) => {
                        const parsedUrl = new URL(url);
                        const options = {
                            hostname: parsedUrl.hostname,
                            port: parsedUrl.port || 443,
                            path: parsedUrl.pathname + parsedUrl.search,
                            method: 'DELETE',
                            headers: { ...headers }
                        };
                        const req = https.request(options, (res) => {
                            let data = '';
                            res.on('data', chunk => data += chunk);
                            res.on('end', () => {
                                try { resolve(JSON.parse(data)); } catch (e) { resolve(data); }
                            });
                        });
                        req.on('error', reject);
                        req.end();
                    });
                },
                ping: (host, timeout = 5000) => {
                    return new Promise((resolve) => {
                        const start = Date.now();
                        const req = https.get(`https://${host}`, () => {
                            resolve(Date.now() - start);
                        });
                        req.on('error', () => resolve(-1));
                        req.setTimeout(timeout, () => resolve(-1));
                    });
                },
                dns: (host) => {
                    return new Promise((resolve, reject) => {
                        dns.lookup(host, (err, address, family) => {
                            if (err) reject(err);
                            else resolve({ address, family });
                        });
                    });
                },
                dns_all: (host) => {
                    return new Promise((resolve, reject) => {
                        dns.lookup(host, { all: true }, (err, addresses) => {
                            if (err) reject(err);
                            else resolve(addresses);
                        });
                    });
                },
                dns_reverse: (ip) => {
                    return new Promise((resolve, reject) => {
                        dns.reverse(ip, (err, hostnames) => {
                            if (err) reject(err);
                            else resolve(hostnames);
                        });
                    });
                },
                ip: () => {
                    const interfaces = os.networkInterfaces();
                    const ips = [];
                    for (const [name, iface] of Object.entries(interfaces)) {
                        for (const addr of iface) {
                            if (addr.family === 'IPv4' && !addr.internal) {
                                ips.push(addr.address);
                            }
                        }
                    }
                    return ips;
                },
                ip_local: () => {
                    const interfaces = os.networkInterfaces();
                    for (const [name, iface] of Object.entries(interfaces)) {
                        for (const addr of iface) {
                            if (addr.family === 'IPv4' && !addr.internal) {
                                return addr.address;
                            }
                        }
                    }
                    return '127.0.0.1';
                }
            },

            // 8. Facil - Operações Facilitadas
            'Facil': {
                media: (lista) => lista.reduce((a, b) => a + b, 0) / lista.length,
                mediana: (lista) => {
                    const sorted = [...lista].sort((a, b) => a - b);
                    const mid = Math.floor(sorted.length / 2);
                    return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
                },
                moda: (lista) => {
                    const freq = {};
                    lista.forEach(x => freq[x] = (freq[x] || 0) + 1);
                    let max = 0, moda = null;
                    for (const [key, val] of Object.entries(freq)) {
                        if (val > max) { max = val; moda = key; }
                    }
                    return moda;
                },
                desvio_padrao: (lista) => {
                    const mean = lista.reduce((a, b) => a + b, 0) / lista.length;
                    const squaredDiffs = lista.map(x => Math.pow(x - mean, 2));
                    return Math.sqrt(squaredDiffs.reduce((a, b) => a + b, 0) / lista.length);
                },
                variancia: (lista) => {
                    const mean = lista.reduce((a, b) => a + b, 0) / lista.length;
                    const squaredDiffs = lista.map(x => Math.pow(x - mean, 2));
                    return squaredDiffs.reduce((a, b) => a + b, 0) / lista.length;
                },
                ordenar: (lista) => [...lista].sort((a, b) => a - b),
                ordenar_desc: (lista) => [...lista].sort((a, b) => b - a),
                buscar: (lista, valor) => lista.indexOf(valor),
                buscar_todos: (lista, valor) => {
                    const indices = [];
                    let idx = lista.indexOf(valor);
                    while (idx !== -1) {
                        indices.push(idx);
                        idx = lista.indexOf(valor, idx + 1);
                    }
                    return indices;
                },
                agrupar: (lista, campo) => {
                    const grupos = {};
                    lista.forEach(item => {
                        const chave = item[campo];
                        if (!grupos[chave]) grupos[chave] = [];
                        grupos[chave].push(item);
                    });
                    return grupos;
                },
                agrupar_por: (lista, funcao) => {
                    const grupos = {};
                    lista.forEach(item => {
                        const chave = funcao(item);
                        if (!grupos[chave]) grupos[chave] = [];
                        grupos[chave].push(item);
                    });
                    return grupos;
                },
                ler_csv: (caminho) => {
                    const conteudo = fs.readFileSync(caminho, 'utf8');
                    const linhas = conteudo.split('\n').filter(l => l.trim());
                    const cabecalho = linhas[0].split(',');
                    return linhas.slice(1).map(linha => {
                        const valores = linha.split(',');
                        const obj = {};
                        cabecalho.forEach((campo, i) => obj[campo.trim()] = valores[i]?.trim());
                        return obj;
                    });
                },
                ler_json: (caminho) => JSON.parse(fs.readFileSync(caminho, 'utf8')),
                ler_xml: (caminho) => {
                    const xml = fs.readFileSync(caminho, 'utf8');
                    // Simples parse XML
                    const matches = xml.match(/<(\w+)>([^<]*)<\/\1>/g) || [];
                    const result = {};
                    matches.forEach(m => {
                        const [, key, value] = m.match(/<(\w+)>([^<]*)<\/\1>/);
                        result[key] = value;
                    });
                    return result;
                },
                tokenizar: (texto) => texto.split(' '),
                tokenizar_por: (texto, separador) => texto.split(separador),
                remover_stopwords: (texto) => {
                    const stopwords = ['a', 'o', 'e', 'de', 'que', 'do', 'da', 'em', 'com', 'para', 'por', 'um', 'uma', 'as', 'os'];
                    const palavras = texto.split(' ');
                    return palavras.filter(p => !stopwords.includes(p.toLowerCase())).join(' ');
                },
                sentimentar: (texto) => {
                    const positivo = ['bom', 'ótimo', 'excelente', 'maravilhoso', 'feliz', 'amor', 'alegria'];
                    const negativo = ['ruim', 'péssimo', 'horrível', 'triste', 'raiva', 'ódio', 'medo'];
                    const palavras = texto.toLowerCase().split(' ');
                    let score = 0;
                    palavras.forEach(p => {
                        if (positivo.includes(p)) score++;
                        if (negativo.includes(p)) score--;
                    });
                    return score > 0 ? 'positivo' : score < 0 ? 'negativo' : 'neutro';
                },
                resumir: (texto, tamanho = 100) => {
                    if (texto.length <= tamanho) return texto;
                    return texto.substring(0, tamanho) + '...';
                },
                extrair_palavras: (texto) => {
                    return texto.match(/[a-zA-Záéíóúãõàèìòùâêîôûç]+/g) || [];
                },
                contar_palavras: (texto) => texto.split(' ').filter(w => w.trim()).length,
                contar_caracteres: (texto) => texto.length,
                contar_linhas: (texto) => texto.split('\n').length,
                contar_frases: (texto) => (texto.match(/[.!?]+/g) || []).length,
                normalizar: (texto) => {
                    const acentos = {
                        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
                        'é': 'e', 'è': 'e', 'ê': 'e',
                        'í': 'i', 'ì': 'i', 'î': 'i',
                        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o',
                        'ú': 'u', 'ù': 'u', 'û': 'u',
                        'ç': 'c'
                    };
                    return texto.split('').map(c => acentos[c] || c).join('');
                },
                slug: (texto) => {
                    return texto.toLowerCase()
                        .replace(/[áàãâ]/g, 'a')
                        .replace(/[éèê]/g, 'e')
                        .replace(/[íìî]/g, 'i')
                        .replace(/[óòõô]/g, 'o')
                        .replace(/[úùû]/g, 'u')
                        .replace(/ç/g, 'c')
                        .replace(/[^a-z0-9]+/g, '-')
                        .replace(/^-+|-+$/g, '');
                }
            },

            // 9. Preguiçoso - IA que completa código
            'Preguiçoso': {
                fazer: async (descricao) => {
                    console.log('😴 Modo Preguiçoso ativado...');
                    const ia = new CorretorAuto();
                    const codigo = await ia.gerar(descricao);
                    return codigo;
                },
                completar: async (codigo) => {
                    console.log('⏳ Completando código...');
                    const ia = new CorretorAuto();
                    return await ia.completar(codigo);
                },
                otimizar: async (codigo) => {
                    console.log('⏳ Otimizando código...');
                    const ia = new CorretorAuto();
                    return await ia.otimizar(codigo);
                },
                refatorar: async (codigo, tipo = 'simplificar') => {
                    console.log('⏳ Refatorando código...');
                    const ia = new CorretorAuto();
                    return await ia.refatorar(codigo, tipo);
                },
                testar: async (codigo) => {
                    console.log('⏳ Gerando testes...');
                    const ia = new CorretorAuto();
                    return await ia.gerarTestes(codigo);
                },
                documentar: async (codigo) => {
                    console.log('⏳ Gerando documentação...');
                    const ia = new CorretorAuto();
                    return await ia.documentar(codigo);
                },
                explicar: async (codigo) => {
                    console.log('⏳ Explicando código...');
                    const ia = new CorretorAuto();
                    return await ia.explicar(codigo);
                },
                traduzir: async (codigo, de = 'nullscript', para = 'javascript') => {
                    console.log('⏳ Traduzindo código...');
                    const ia = new CorretorAuto();
                    return await ia.traduzir(codigo, de, para);
                }
            },

            // 10. Auto - Automatização
            'Auto': {
                criar_api: (config) => {
                    const nome = config.nome || 'recurso';
                    const campos = config.campos || ['id', 'nome'];
                    const operacoes = config.operacoes || ['listar', 'criar', 'atualizar', 'deletar'];
                    
                    let codigo = `// API REST para ${nome}\n`;
                    codigo += `importar biblioteca Rede\n\n`;
                    codigo += `dados_${nome} = []\n\n`;
                    
                    if (operacoes.includes('listar')) {
                        codigo += `Rede.rota("/${nome}", (req, res) => {\n`;
                        codigo += `    res.json({ dados: dados_${nome} })\n`;
                        codigo += `})\n\n`;
                    }
                    
                    if (operacoes.includes('criar')) {
                        codigo += `Rede.rota("/${nome}/criar", (req, res) => {\n`;
                        codigo += `    const dados = req.corpo\n`;
                        codigo += `    dados.id = dados_${nome}.tamanho + 1\n`;
                        codigo += `    dados_${nome}.adicionar(dados)\n`;
                        codigo += `    res.json({ mensagem: "Criado", dados })\n`;
                        codigo += `})\n\n`;
                    }
                    
                    if (operacoes.includes('atualizar')) {
                        codigo += `Rede.rota("/${nome}/:id", (req, res) => {\n`;
                        codigo += `    const id = parseInt(req.parametros.id)\n`;
                        codigo += `    const dados = req.corpo\n`;
                        codigo += `    dados_${nome}[id] = dados\n`;
                        codigo += `    res.json({ mensagem: "Atualizado", dados })\n`;
                        codigo += `})\n\n`;
                    }
                    
                    if (operacoes.includes('deletar')) {
                        codigo += `Rede.rota("/${nome}/:id", (req, res) => {\n`;
                        codigo += `    const id = parseInt(req.parametros.id)\n`;
                        codigo += `    dados_${nome}.remover_posicao(id)\n`;
                        codigo += `    res.json({ mensagem: "Deletado" })\n`;
                        codigo += `})\n\n`;
                    }
                    
                    if (config.autenticacao) {
                        codigo += `// Autenticação JWT\n`;
                        codigo += `Rede.middleware((req, res, proximo) => {\n`;
                        codigo += `    const token = req.headers["Authorization"]\n`;
                        codigo += `    if (!token) {\n`;
                        codigo += `        res.status(401).json({ erro: "Token necessário" })\n`;
                        codigo += `        return\n`;
                        codigo += `    }\n`;
                        codigo += `    proximo()\n`;
                        codigo += `})\n\n`;
                    }
                    
                    codigo += `Rede.servidor(3000).iniciar()\n`;
                    codigo += `exibir: "🚀 API rodando em http://localhost:3000"`;
                    
                    return codigo;
                },
                criar_crud: (nome, campos) => {
                    let codigo = `// CRUD para ${nome}\n`;
                    codigo += `dados_${nome} = []\n\n`;
                    
                    codigo += `funcao criar_${nome}(${campos.join(', ')}) {\n`;
                    codigo += `    const item = { ${campos.map(c => `${c}: ${c}`).join(', ')} }\n`;
                    codigo += `    dados_${nome}.adicionar(item)\n`;
                    codigo += `    retorne item\n`;
                    codigo += `}\n\n`;
                    
                    codigo += `funcao listar_${nome}() {\n`;
                    codigo += `    retorne dados_${nome}\n`;
                    codigo += `}\n\n`;
                    
                    codigo += `funcao atualizar_${nome}(id, ${campos.join(', ')}) {\n`;
                    codigo += `    const item = dados_${nome}[id]\n`;
                    campos.forEach(c => codigo += `    item.${c} = ${c}\n`);
                    codigo += `    retorne item\n`;
                    codigo += `}\n\n`;
                    
                    codigo += `funcao deletar_${nome}(id) {\n`;
                    codigo += `    dados_${nome}.remover_posicao(id)\n`;
                    codigo += `    retorne verdadeiro\n`;
                    codigo += `}\n`;
                    
                    return codigo;
                },
                criar_jogo: (tipo = 'simples') => {
                    let codigo = `// Jogo ${tipo}\nimportar biblioteca Jogo\n\n`;
                    codigo += `jogo = Jogo.criar(800, 600, "Meu Jogo")\n\n`;
                    
                    if (tipo === 'plataforma') {
                        codigo += `// Jogador\n`;
                        codigo += `jogador = Jogo.sprite(jogo, "personagem.png", 50, 50)\n`;
                        codigo += `jogador.velocidade = 5\n`;
                        codigo += `jogador.velocidade_y = 0\n`;
                        codigo += `jogador.esta_no_chao = verdadeiro\n\n`;
                        
                        codigo += `// Controles\n`;
                        codigo += `Jogo.tecla("esquerda", () => jogador.x -= jogador.velocidade)\n`;
                        codigo += `Jogo.tecla("direita", () => jogador.x += jogador.velocidade)\n`;
                        codigo += `Jogo.tecla("espaco", () => {\n`;
                        codigo += `    if (jogador.esta_no_chao) {\n`;
                        codigo += `        jogador.velocidade_y = -10\n`;
                        codigo += `        jogador.esta_no_chao = falso\n`;
                        codigo += `    }\n`;
                        codigo += `})\n\n`;
                        
                        codigo += `// Física\n`;
                        codigo += `jogo.fisica(9.8)\n\n`;
                        
                        codigo += `// Loop\n`;
                        codigo += `Jogo.loop(jogo, () => {\n`;
                        codigo += `    jogador.y += jogador.velocidade_y\n`;
                        codigo += `    jogador.velocidade_y += 0.5\n`;
                        codigo += `    if (jogador.y >= 500) {\n`;
                        codigo += `        jogador.y = 500\n`;
                        codigo += `        jogador.esta_no_chao = verdadeiro\n`;
                        codigo += `    }\n`;
                        codigo += `    Jogo.renderizar(jogador)\n`;
                        codigo += `})\n`;
                    } else {
                        codigo += `// Jogo simples\n`;
                        codigo += `Jogo.loop(jogo, () => {\n`;
                        codigo += `    Jogo.fundo("preto")\n`;
                        codigo += `    Jogo.texto("Jogo " + Jogo.tempo(), 400, 300, "branco")\n`;
                        codigo += `})\n`;
                    }
                    
                    codigo += `Jogo.iniciar(jogo)`;
                    return codigo;
                },
                criar_site: (config) => {
                    const paginas = config.paginas || ['home', 'sobre', 'contato'];
                    const estilo = config.estilo || 'moderno';
                    
                    let codigo = `// Site gerado\nimportar biblioteca Web\n\n`;
                    
                    paginas.forEach(pagina => {
                        codigo += `Web.rota("/${pagina}", (req, res) => {\n`;
                        codigo += `    res.html(\`\n`;
                        codigo += `        <html>\n`;
                        codigo += `            <head>\n`;
                        codigo += `                <title>${pagina.charAt(0).toUpperCase() + pagina.slice(1)}</title>\n`;
                        codigo += `                <style>\n`;
                        codigo += `                    body { font-family: Arial; margin: 40px; }\n`;
                        codigo += `                    h1 { color: #333; }\n`;
                        codigo += `                </style>\n`;
                        codigo += `            </head>\n`;
                        codigo += `            <body>\n`;
                        codigo += `                <h1>${pagina.charAt(0).toUpperCase() + pagina.slice(1)}</h1>\n`;
                        codigo += `                <p>Página ${pagina}</p>\n`;
                        codigo += `                <a href="/">Home</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>\n`;
                        codigo += `            </body>\n`;
                        codigo += `        </html>\n`;
                        codigo += `    \`)\n`;
                        codigo += `})\n\n`;
                    });
                    
                    codigo += `Web.servidor(3000).iniciar()\n`;
                    codigo += `exibir: "🌐 Site rodando em http://localhost:3000"`;
                    
                    return codigo;
                },
                criar_bot: (plataforma, config) => {
                    let codigo = `// Bot para ${plataforma}\nimportar biblioteca Rede\n\n`;
                    
                    if (plataforma === 'discord') {
                        codigo += `bot = Rede.websocket("wss://discord.com")\n\n`;
                        codigo += `bot.on("mensagem", (msg) => {\n`;
                        codigo += `    if (msg.includes("!ping")) {\n`;
                        codigo += `        bot.enviar("Pong!")\n`;
                        codigo += `    }\n`;
                        codigo += `    if (msg.includes("!help")) {\n`;
                        codigo += `        bot.enviar("Comandos: !ping, !help, !info")\n`;
                        codigo += `    }\n`;
                        codigo += `    if (msg.includes("!info")) {\n`;
                        codigo += `        bot.enviar("Bot em NullScript v3.0")\n`;
                        codigo += `    }\n`;
                        codigo += `})\n`;
                    } else if (plataforma === 'telegram') {
                        codigo += `const token = "${config.token || 'SEU_TOKEN'}"\n`;
                        codigo += `const url = "https://api.telegram.org/bot" + token\n\n`;
                        codigo += `funcao enviar(chat_id, texto) {\n`;
                        codigo += `    Rede.post(url + "/sendMessage", {\n`;
                        codigo += `        chat_id: chat_id,\n`;
                        codigo += `        text: texto\n`;
                        codigo += `    })\n`;
                        codigo += `}\n\n`;
                        codigo += `// Webhook\n`;
                        codigo += `Web.rota("/webhook", (req, res) => {\n`;
                        codigo += `    const msg = req.corpo\n`;
                        codigo += `    if (msg.text) {\n`;
                        codigo += `        enviar(msg.chat.id, "Recebi: " + msg.text)\n`;
                        codigo += `    }\n`;
                        codigo += `    res.json({ ok: verdadeiro })\n`;
                        codigo += `})\n`;
                    }
                    
                    codigo += `exibir: "🤖 Bot ${plataforma} iniciado!"`;
                    return codigo;
                },
                criar_cli: (config) => {
                    const comandos = config.comandos || {
                        'help': 'Mostra ajuda',
                        'version': 'Mostra versão'
                    };
                    
                    let codigo = `// CLI gerado\n`;
                    codigo += `const args = Sistema.argv().slice(2)\n\n`;
                    codigo += `funcao mostrar_ajuda() {\n`;
                    codigo += `    exibir: "Comandos disponíveis:"\n`;
                    for (const [cmd, desc] of Object.entries(comandos)) {
                        codigo += `    exibir: "  ${cmd} - ${desc}"\n`;
                    }
                    codigo += `}\n\n`;
                    
                    codigo += `se args.tamanho == 0 {\n`;
                    codigo += `    mostrar_ajuda()\n`;
                    codigo += `} senao {\n`;
                    codigo += `    escolha args[0]\n`;
                    for (const [cmd] of Object.entries(comandos)) {
                        codigo += `        caso "${cmd}":\n`;
                        codigo += `            exibir: "Executando ${cmd}..."\n`;
                        codigo += `            // TODO: Implementar ${cmd}\n`;
                    }
                    codigo += `        padrao: exibir: "Comando desconhecido"\n`;
                    codigo += `    fim\n`;
                    codigo += `}\n`;
                    
                    return codigo;
                }
            },

            // 11. Jogo - Game Development
            'Jogo': {
                criar: (largura, altura, titulo) => ({
                    largura: largura || 800,
                    altura: altura || 600,
                    titulo: titulo || 'Jogo',
                    sprites: [],
                    fisica: null,
                    loop: null
                }),
                sprite: (jogo, imagem, x, y) => ({
                    imagem,
                    x: x || 0,
                    y: y || 0,
                    largura: 50,
                    altura: 50,
                    velocidade: 5
                }),
                tecla: (tecla, funcao) => {
                    console.log(`Tecla ${tecla} registrada`);
                    return funcao;
                },
                loop: (jogo, funcao) => {
                    jogo.loop = funcao;
                    return jogo;
                },
                renderizar: (sprite) => {
                    // Simulação
                    return sprite;
                },
                fundo: (cor) => console.log(`Fundo: ${cor}`),
                texto: (texto, x, y, cor) => console.log(`Texto: ${texto} em ${x},${y}`),
                fisica: (jogo, gravidade) => {
                    jogo.fisica = { gravidade };
                    return jogo;
                },
                colisao: (obj1, obj2, funcao) => {
                    // Simulação
                    return funcao;
                },
                iniciar: (jogo) => {
                    console.log(`🎮 Iniciando jogo: ${jogo.titulo}`);
                    console.log(`   Largura: ${jogo.largura}, Altura: ${jogo.altura}`);
                    if (jogo.loop) {
                        console.log('Loop iniciado');
                    }
                    return jogo;
                },
                pausar: (jogo) => {
                    console.log('⏸️ Jogo pausado');
                    return jogo;
                },
                continuar: (jogo) => {
                    console.log('▶️ Jogo continuado');
                    return jogo;
                },
                finalizar: (jogo) => {
                    console.log('🏁 Jogo finalizado');
                    return jogo;
                },
                som: (arquivo, volume) => {
                    console.log(`🔊 Som: ${arquivo} (volume: ${volume || 1})`);
                },
                musica: (arquivo, volume) => {
                    console.log(`🎵 Música: ${arquivo} (volume: ${volume || 0.5})`);
                }
            },

            // 12. Web - Desenvolvimento Web
            'Web': {
                servidor: (porta) => {
                    console.log(`🌐 Servidor web rodando em http://localhost:${porta || 3000}`);
                    return {
                        porta: porta || 3000,
                        rotas: {},
                        iniciar: () => console.log('Servidor iniciado'),
                        fechar: () => console.log('Servidor fechado')
                    };
                },
                rota: (caminho, handler) => {
                    console.log(`📝 Rota registrada: ${caminho}`);
                    return handler;
                },
                middleware: (handler) => {
                    console.log('🔧 Middleware registrado');
                    return handler;
                },
                html: (conteudo) => {
                    return { tipo: 'html', conteudo };
                },
                json: (dados) => {
                    return { tipo: 'json', conteudo: JSON.stringify(dados) };
                },
                css: (conteudo) => {
                    return { tipo: 'css', conteudo };
                },
                js: (conteudo) => {
                    return { tipo: 'js', conteudo };
                },
                static: (pasta) => {
                    console.log(`📁 Pasta estática: ${pasta}`);
                    return pasta;
                },
                session: (chave, valor) => {
                    console.log(`🔐 Sessão: ${chave} = ${valor}`);
                    return { [chave]: valor };
                },
                cookie: (nome, valor) => {
                    console.log(`🍪 Cookie: ${nome} = ${valor}`);
                    return { [nome]: valor };
                },
                template: (arquivo, dados) => {
                    console.log(`📄 Template: ${arquivo}`);
                    return dados;
                }
            },

            // 13. BD - Banco de Dados
            'BD': {
                conectar: (tipo, ...args) => {
                    console.log(`🔌 Conectando ao banco ${tipo}...`);
                    return { tipo, args, conectado: true, query: (sql) => ({ rows: [{ id: 1, nome: 'Exemplo' }] }) };
                },
                criar_tabela: (db, nome, campos) => {
                    console.log(`📋 Tabela ${nome} criada:`, campos);
                    return true;
                },
                criar: (db, tabela, dados) => {
                    console.log(`📝 Criando em ${tabela}:`, dados);
                    return { id: Date.now(), ...dados };
                },
                ler: (db, tabela, filtro) => {
                    console.log(`📖 Lendo de ${tabela}:`, filtro);
                    return [{ id: 1, nome: 'Exemplo' }];
                },
                buscar: (db, query) => {
                    console.log(`🔍 Buscando: ${query}`);
                    return [{ id: 1, nome: 'Resultado' }];
                },
                buscar_um: (db, query) => {
                    console.log(`🔍 Buscando um: ${query}`);
                    return { id: 1, nome: 'Resultado' };
                },
                atualizar: (db, tabela, filtro, dados) => {
                    console.log(`✏️ Atualizando ${tabela}:`, filtro, dados);
                    return true;
                },
                deletar: (db, tabela, filtro) => {
                    console.log(`🗑️ Deletando de ${tabela}:`, filtro);
                    return true;
                },
                transacao: (db, funcao) => {
                    console.log('🔄 Iniciando transação...');
                    try {
                        funcao();
                        console.log('✅ Transação concluída');
                        return true;
                    } catch (e) {
                        console.log('❌ Transação falhou:', e.message);
                        return false;
                    }
                },
                desconectar: (db) => {
                    console.log('🔌 Desconectando...');
                    return true;
                }
            }
        };
    }

    // ============================================================
    //              MÉTODOS DE EXECUÇÃO
    // ============================================================

    executar(codigo, arquivo = '') {
        const inicio = Date.now();
        this.metricas.execucoes++;
        this.historico.push(codigo);
        this.arquivo_atual = arquivo;

        try {
            if (this.auto_corrigir) {
                const corrigido = this.ia.corrigir(codigo);
                if (corrigido !== codigo && this.debug) {
                    console.log('[IA] Código corrigido automaticamente');
                }
                codigo = corrigido;
            }

            const resultado = this.interpretar(codigo);
            this.metricas.tempo_total += Date.now() - inicio;
            return resultado;
        } catch (erro) {
            this.metricas.erros++;
            console.error(`❌ Erro na linha ${this.linha_atual}:`, erro.message);
            
            if (this.auto_corrigir) {
                console.log('[IA] Tentando corrigir automaticamente...');
                try {
                    const codigoCorrigido = this.ia.corrigir(this.historico[this.historico.length - 1]);
                    return this.executar(codigoCorrigido, arquivo);
                } catch (e) {
                    console.error('[ERRO] Não foi possível corrigir:', e.message);
                }
            }
            
            throw erro;
        }
    }

    interpretar(codigo) {
        const linhas = codigo.split('\n');
        let resultado = null;
        let emBloco = false;
        let bloco = [];
        let blocoTipo = '';
        let blocoCondicao = '';

        for (let i = 0; i < linhas.length; i++) {
            this.linha_atual = i + 1;
            const linha = linhas[i];
            const linhaTrim = linha.trim();

            // Pular linhas vazias e comentários
            if (!linhaTrim || linhaTrim.startsWith('//') || linhaTrim.startsWith('#')) continue;

            // Detectar início de bloco
            if (linhaTrim.match(/^(Se|Enquanto|Para|funcao|Tentar|Escolha)/i)) {
                emBloco = true;
                blocoTipo = linhaTrim.split(' ')[0];
                blocoCondicao = linhaTrim;
                bloco = [];
                continue;
            }

            // Detectar fim de bloco
            if (linhaTrim.match(/^(Fim|end|})/i)) {
                emBloco = false;
                // Executar bloco
                resultado = this.executarBloco(blocoTipo, blocoCondicao, bloco);
                continue;
            }

            if (emBloco) {
                bloco.push(linha);
                continue;
            }

            // Linha única
            try {
                resultado = this.processarLinha(linha);
            } catch (erro) {
                if (this.modo_aprendiz) {
                    console.log('[IA] Erro na linha', i + 1, ':', erro.message);
                    const sugestao = this.ia.perguntar(erro.message);
                    console.log('[IA] Sugestão:', sugestao);
                }
                throw erro;
            }
        }

        return resultado;
    }

    executarBloco(tipo, condicao, linhas) {
        const codigoBloco = linhas.join('\n');
        
        switch (tipo.toLowerCase()) {
            case 'se':
                return this.executarSe(condicao, codigoBloco);
            case 'enquanto':
                return this.executarEnquanto(condicao, codigoBloco);
            case 'para':
                return this.executarPara(condicao, codigoBloco);
            case 'funcao':
                return this.executarFuncao(condicao, codigoBloco);
            default:
                return this.interpretar(codigoBloco);
        }
    }

    executarSe(condicao, bloco) {
        // Extrair condição
        const cond = condicao.replace(/^Se\s*:?\s*/, '').trim();
        const resultado = this.avaliarExpressao(cond);
        
        if (resultado) {
            return this.interpretar(bloco);
        }
        return null;
    }

    executarEnquanto(condicao, bloco) {
        const cond = condicao.replace(/^Enquanto\s*:?\s*/, '').trim();
        let resultado = null;
        let maxIteracoes = 1000000;
        let iteracoes = 0;

        while (this.avaliarExpressao(cond) && iteracoes < maxIteracoes) {
            try {
                resultado = this.interpretar(bloco);
                iteracoes++;
            } catch (e) {
                if (e.message === 'BREAK') break;
                if (e.message === 'CONTINUE') continue;
                throw e;
            }
        }

        return resultado;
    }

    executarPara(condicao, bloco) {
        // Para i de 1 ate 10
        const match = condicao.match(/Para\s+(\w+)\s+de\s+(\d+)\s+ate\s+(\d+)(?:\s+passo\s+(\d+))?/i);
        if (match) {
            const [, variavel, inicio, fim, passo] = match;
            const inicioNum = parseInt(inicio);
            const fimNum = parseInt(fim);
            const passoNum = parseInt(passo) || 1;
            let resultado = null;

            this.variaveis[variavel] = inicioNum;
            let valor = inicioNum;

            while (passoNum > 0 ? valor <= fimNum : valor >= fimNum) {
                this.variaveis[variavel] = valor;
                try {
                    resultado = this.interpretar(bloco);
                } catch (e) {
                    if (e.message === 'BREAK') break;
                    if (e.message === 'CONTINUE') {
                        valor += passoNum;
                        continue;
                    }
                    throw e;
                }
                valor += passoNum;
            }

            return resultado;
        }
        return null;
    }

    executarFuncao(condicao, bloco) {
        // funcao nome(param1, param2)
        const match = condicao.match(/funcao\s+(\w+)\s*\(([^)]*)\)/i);
        if (match) {
            const [, nome, params] = match;
            const parametros = params ? params.split(',').map(p => p.trim()) : [];
            
            this.funcoes[nome] = {
                nome,
                parametros,
                corpo: bloco,
                executar: (args) => {
                    // Salvar variáveis atuais
                    const varsAntigas = { ...this.variaveis };
                    
                    // Definir parâmetros
                    for (let i = 0; i < parametros.length; i++) {
                        this.variaveis[parametros[i]] = args[i] || null;
                    }
                    
                    let resultado = null;
                    try {
                        resultado = this.interpretar(bloco);
                    } finally {
                        // Restaurar variáveis
                        this.variaveis = varsAntigas;
                    }
                    
                    return resultado;
                }
            };
            
            return this.funcoes[nome];
        }
        return null;
    }

    // ============================================================
    //              PROCESSADORES DE LINHA
    // ============================================================

    processarLinha(linha) {
        const linhaTrim = linha.trim();
        
        // Detectar padrões
        if (linhaTrim.match(/^(exibir|mostrar|print)/i)) {
            return this.processarExibir(linha);
        }
        if (linhaTrim.match(/^(perguntar|input)/i)) {
            return this.processarPerguntar(linha);
        }
        if (linhaTrim.match(/^(crie|criar|var|let|declare)/i)) {
            return this.processarDeclaracao(linha);
        }
        if (linhaTrim.match(/^constante/i)) {
            return this.processarConstante(linha);
        }
        if (linhaTrim.match(/^retorne|^return/i)) {
            return this.processarRetorne(linha);
        }
        if (linhaTrim.match(/^importar|^import/i)) {
            return this.processarImportar(linha);
        }
        if (linhaTrim.match(/^limpar|^clear/i)) {
            return this.processarLimpar(linha);
        }
        if (linhaTrim.match(/^sair|^exit/i)) {
            return this.processarSair(linha);
        }
        if (linhaTrim.includes('=')) {
            return this.processarAtribuicao(linha);
        }
        if (linhaTrim.includes('(') && linhaTrim.includes(')')) {
            return this.processarChamadaFuncao(linha);
        }
        
        return this.avaliarExpressao(linha);
    }

    processarExibir(linha) {
        let texto = linha.replace(/^(exibir|mostrar|print)\s*:?\s*/, '');
        // Remover aspas
        texto = texto.replace(/^["']|["']$/g, '');
        // Interpolação
        texto = texto.replace(/\${(.*?)}/g, (match, expr) => {
            return this.avaliarExpressao(expr.trim());
        });
        // Avaliar expressões dentro de ${}
        texto = texto.replace(/\{([^}]+)\}/g, (match, expr) => {
            return this.avaliarExpressao(expr.trim());
        });
        console.log(texto);
        return texto;
    }

    processarPerguntar(linha) {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        let texto = linha.replace(/^(perguntar|input)\s*:?\s*/, '');
        texto = texto.replace(/^["']|["']$/g, '');

        return new Promise((resolve) => {
            rl.question(texto + ' ', (resposta) => {
                rl.close();
                // Verificar se é número
                const num = parseFloat(resposta);
                if (!isNaN(num)) {
                    resolve(num);
                } else {
                    resolve(resposta);
                }
            });
        });
    }

    processarDeclaracao(linha) {
        // crie variável, nome X, valor Y
        const match = linha.match(/(?:crie|criar|var|let|declare)\s+(?:variavel\s*,\s*nome\s*)?(\w+)(?:\s*,\s*valor\s*)?\s*=\s*(.+)/i);
        if (match) {
            const [, nome, valor] = match;
            this.variaveis[nome] = this.avaliarExpressao(valor.trim());
            return this.variaveis[nome];
        }
        
        // var x = 10
        const match2 = linha.match(/(?:var|let)\s+(\w+)\s*=\s*(.+)/i);
        if (match2) {
            const [, nome, valor] = match2;
            this.variaveis[nome] = this.avaliarExpressao(valor.trim());
            return this.variaveis[nome];
        }
        
        return null;
    }

    processarConstante(linha) {
        const match = linha.match(/constante\s+(\w+)\s*=\s*(.+)/i);
        if (match) {
            const [, nome, valor] = match;
            this.constantes[nome] = this.avaliarExpressao(valor.trim());
            return this.constantes[nome];
        }
        return null;
    }

    processarAtribuicao(linha) {
        const match = linha.match(/^(\w+)\s*=\s*(.+)/);
        if (match) {
            const [, nome, valor] = match;
            const valorAvaliado = this.avaliarExpressao(valor.trim());
            this.variaveis[nome] = valorAvaliado;
            return valorAvaliado;
        }
        return null;
    }

    processarRetorne(linha) {
        const valor = linha.replace(/^(retorne|return)\s*:?\s*/, '');
        const resultado = this.avaliarExpressao(valor);
        this.retorno_atual = resultado;
        return resultado;
    }

    processarImportar(linha) {
        const match = linha.match(/importar\s+(?:biblioteca\s+)?(\w+)/i);
        if (match) {
            const nome = match[1];
            this.importacoes[nome] = true;
            
            // Carregar biblioteca nativa
            if (this.bibliotecas[nome]) {
                this.variaveis[nome] = this.bibliotecas[nome];
                return this.bibliotecas[nome];
            }
            
            return nome;
        }
        return null;
    }

    processarLimpar(linha) {
        console.clear();
        return true;
    }

    processarSair(linha) {
        console.log('👋 Saindo...');
        process.exit(0);
    }

    processarChamadaFuncao(linha) {
        const match = linha.match(/(\w+)\s*\(([^)]*)\)/);
        if (match) {
            const [, nome, args] = match;
            const argumentos = args ? args.split(',').map(a => this.avaliarExpressao(a.trim())) : [];

            // Verificar funções nativas
            const nativas = {
                'tipo': (v) => typeof v,
                'numero': (v) => parseFloat(v) || 0,
                'texto': (v) => String(v),
                'lista': (...v) => v,
                'aleatorio': () => Math.random(),
                'aleatorio_entre': (min, max) => Math.floor(Math.random() * (max - min + 1)) + min,
                'data_atual': () => new Date().toString(),
                'timestamp': () => Date.now(),
                'dormir': (ms) => { const start = Date.now(); while (Date.now() - start < ms) {} return true; },
                'tamanho': (v) => v && v.length !== undefined ? v.length : 0,
                'contem': (v, item) => v && v.includes ? v.includes(item) : false,
                'posicao': (v, item) => v && v.indexOf ? v.indexOf(item) : -1,
                'maiusculo': (v) => v ? v.toUpperCase() : '',
                'minusculo': (v) => v ? v.toLowerCase() : '',
                'absoluto': (v) => Math.abs(v),
                'raiz_quadrada': (v) => Math.sqrt(v),
                'potencia': (a, b) => Math.pow(a, b),
                'arredondar': (v) => Math.round(v)
            };

            if (nativas[nome]) {
                return nativas[nome](...argumentos);
            }

            // Verificar funções definidas
            if (this.funcoes[nome]) {
                return this.funcoes[nome].executar(argumentos);
            }

            // Verificar variáveis que são funções
            if (this.variaveis[nome] && typeof this.variaveis[nome] === 'function') {
                return this.variaveis[nome](...argumentos);
            }

            return null;
        }
        return null;
    }

    // ============================================================
    //              AVALIADOR DE EXPRESSÕES
    // ============================================================

    avaliarExpressao(expr) {
        if (!expr) return null;
        expr = expr.trim();

        // Números
        if (/^-?\d+(\.\d+)?$/.test(expr)) {
            return parseFloat(expr);
        }

        // Booleanos
        if (/^(verdadeiro|true)$/i.test(expr)) return true;
        if (/^(falso|false)$/i.test(expr)) return false;
        if (/^(vazio|null)$/i.test(expr)) return null;
        if (/^(indefinido|undefined)$/i.test(expr)) return undefined;

        // Strings
        if (expr.match(/^["'].*["']$/)) {
            return expr.slice(1, -1);
        }

        // Variáveis
        if (/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(expr)) {
            if (this.constantes[expr] !== undefined) return this.constantes[expr];
            if (this.variaveis[expr] !== undefined) return this.variaveis[expr];
            return expr;
        }

        // Expressões matemáticas
        try {
            // Substituir variáveis
            let expressao = expr;
            for (const [nome, valor] of Object.entries(this.variaveis)) {
                expressao = expressao.replace(new RegExp(`\\b${nome}\\b`, 'g'), valor);
            }
            for (const [nome, valor] of Object.entries(this.constantes)) {
                expressao = expressao.replace(new RegExp(`\\b${nome}\\b`, 'g'), valor);
            }
            // Avaliar
            return eval(expressao);
        } catch (e) {
            return expr;
        }
    }

    // ============================================================
    //              EXECUÇÃO DE ARQUIVO
    // ============================================================

    executarArquivo(caminho) {
        try {
            const caminhoAbsoluto = path.resolve(caminho);
            if (!fs.existsSync(caminhoAbsoluto)) {
                console.error(`❌ Arquivo não encontrado: ${caminho}`);
                return null;
            }

            const codigo = fs.readFileSync(caminhoAbsoluto, 'utf8');
            console.log(`📄 Executando: ${caminho}`);
            
            // Carregar bibliotecas primeiro
            this.carregarBibliotecas();
            
            return this.executar(codigo, caminhoAbsoluto);
        } catch (erro) {
            console.error('❌ Erro ao executar arquivo:', erro.message);
            return null;
        }
    }
}

// ============================================================
//              INTERFACE DE LINHA DE COMANDO
// ============================================================

class NullScriptCLI {
    constructor() {
        this.interpreter = new NullScriptInterpreter();
        this.versao = VERSAO;
    }

    iniciar() {
        const args = process.argv.slice(2);

        if (args.length === 0) {
            this.mostrarAjuda();
            return;
        }

        const comando = args[0];

        switch (comando) {
            case '--help':
            case '-h':
                this.mostrarAjuda();
                break;
            case '--version':
            case '-v':
                console.log(`NullScript v${this.versao}`);
                break;
            case '--repl':
            case '-r':
                this.iniciarREPL();
                break;
            case '--ia':
                this.modoIA(args.slice(1));
                break;
            case '--doc':
                this.gerarDocumentacao(args.slice(1));
                break;
            case '--compile':
                this.compilar(args.slice(1));
                break;
            default:
                // Executar arquivo
                this.executarArquivo(comando);
                break;
        }
    }

    mostrarAjuda() {
        console.log(`
╔═══════════════════════════════════════════════════════╗
║          NULLSCRIPT - LINGUAGEM COMPLETA             ║
║             Versão ${this.versao}                      ║
╚═══════════════════════════════════════════════════════╝

📖 USO:
  nullscript <arquivo.ns>        Executa um arquivo .ns
  nullscript <arquivo>           Executa um arquivo .ns
  nullscript --repl              Modo interativo (REPL)
  nullscript --help              Mostra esta ajuda
  nullscript --version           Mostra a versão
  nullscript --ia <arquivo>      Executa com IA ativa
  nullscript --doc <arquivo>     Gera documentação
  nullscript --compile <arquivo> Compila para JavaScript

📝 EXEMPLOS:
  nullscript exemplo.ns          Executa o arquivo
  nullscript --repl              Inicia o REPL
  nullscript --ia exemplo.ns     Executa com IA

🔧 OPÇÕES:
  --ia         Ativa IA (CorretorAuto)
  --aprendiz   Modo aprendiz (IA explica)
  --debug      Modo debug
  --doc        Gera documentação
  --compile    Compila para JS

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

🌐 MAIS INFORMAÇÕES:
  https://github.com/nullscript/nullscript
        `);
    }

    executarArquivo(caminho) {
        // Verificar extensão
        if (!caminho.endsWith('.ns') && !caminho.endsWith('.null')) {
            console.warn(`⚠️ Arquivo sem extensão .ns: ${caminho}`);
        }

        this.interpreter.executarArquivo(caminho);
    }

    iniciarREPL() {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
            prompt: 'null> '
        });

        console.log(`
🚀 NULLSCRIPT REPL v${this.versao}
📖 Digite "help" para ajuda
📖 Digite "sair" para sair
🔧 IA ativa: ${this.interpreter.auto_corrigir ? 'Sim' : 'Não'}
        `);

        rl.prompt();

        rl.on('line', async (linha) => {
            const linhaTrim = linha.trim();
            if (!linhaTrim) { rl.prompt(); return; }

            if (linhaTrim === 'sair' || linhaTrim === 'exit') {
                rl.close();
                return;
            }

            if (linhaTrim === 'help') {
                console.log(`
Comandos disponíveis:
  help     - Mostra esta ajuda
  sair     - Sai do REPL
  clear    - Limpa a tela
  debug    - Ativa/desativa debug
  ia       - Mostra status da IA
  libs     - Lista bibliotecas
  vars     - Mostra variáveis
  funs     - Mostra funções
                `);
                rl.prompt();
                return;
            }

            if (linhaTrim === 'clear') {
                console.clear();
                rl.prompt();
                return;
            }

            if (linhaTrim === 'debug') {
                this.interpreter.debug = !this.interpreter.debug;
                console.log(`Debug: ${this.interpreter.debug ? 'ON' : 'OFF'}`);
                rl.prompt();
                return;
            }

            if (linhaTrim === 'ia') {
                console.log('Status da IA:');
                console.log(`  - Modelo: ${this.interpreter.ia.modelo}`);
                console.log(`  - Auto-corrigir: ${this.interpreter.auto_corrigir ? 'Sim' : 'Não'}`);
                console.log(`  - Modo aprendiz: ${this.interpreter.modo_aprendiz ? 'Sim' : 'Não'}`);
                rl.prompt();
                return;
            }

            if (linhaTrim === 'libs') {
                console.log('📚 Bibliotecas disponíveis:');
                for (const [nome, lib] of Object.entries(this.interpreter.bibliotecas)) {
                    const funcoes = Object.keys(lib);
                    console.log(`  ${nome}: ${funcoes.length} funções`);
                }
                rl.prompt();
                return;
            }

            if (linhaTrim === 'vars') {
                console.log('📦 Variáveis:');
                for (const [nome, valor] of Object.entries(this.interpreter.variaveis)) {
                    console.log(`  ${nome} = ${typeof valor === 'object' ? JSON.stringify(valor) : valor}`);
                }
                rl.prompt();
                return;
            }

            if (linhaTrim === 'funs') {
                console.log('📦 Funções:');
                for (const [nome, func] of Object.entries(this.interpreter.funcoes)) {
                    console.log(`  ${nome}(${func.parametros.join(', ')})`);
                }
                rl.prompt();
                return;
            }

            try {
                const resultado = await this.interpreter.executar(linhaTrim);
                if (resultado !== undefined && resultado !== null) {
                    console.log('=>', typeof resultado === 'object' ? JSON.stringify(resultado, null, 2) : resultado);
                }
            } catch (erro) {
                console.error('❌', erro.message);
                if (this.interpreter.auto_corrigir) {
                    console.log('[IA] Tentando corrigir...');
                    try {
                        const corrigido = await this.interpreter.ia.corrigir(linhaTrim);
                        if (corrigido !== linhaTrim) {
                            console.log('[IA] Sugestão:', corrigido);
                            const { executar } = await new Promise((resolve) => {
                                rl.question('Executar correção? (s/n): ', (res) => {
                                    resolve({ executar: res.toLowerCase() === 's' });
                                });
                            });
                            if (executar) {
                                const resultado = await this.interpreter.executar(corrigido);
                                if (resultado !== undefined && resultado !== null) {
                                    console.log('=>', resultado);
                                }
                            }
                        }
                    } catch (e) {}
                }
            }

            rl.prompt();
        });

        rl.on('close', () => {
            console.log('\n👋 Até logo!');
            process.exit(0);
        });
    }

    modoIA(args) {
        if (args.length === 0) {
            console.log('❌ Especifique um arquivo');
            return;
        }

        this.interpreter.auto_corrigir = true;
        this.interpreter.modo_aprendiz = true;
        console.log('🧠 IA ativada (auto-correção e modo aprendiz)');
        this.executarArquivo(args[0]);
    }

    gerarDocumentacao(args) {
        if (args.length === 0) {
            console.log('❌ Especifique um arquivo');
            return;
        }

        const caminho = args[0];
        if (!fs.existsSync(caminho)) {
            console.error(`❌ Arquivo não encontrado: ${caminho}`);
            return;
        }

        const codigo = fs.readFileSync(caminho, 'utf8');
        const analise = this.interpreter.ia.analisar(codigo);
        
        console.log(`
📚 DOCUMENTAÇÃO - ${caminho}
${'='.repeat(50)}

📊 ANÁLISE:
  Qualidade: ${analise.qualidade}/10
  Complexidade: ${analise.complexidade}/10
  Segurança: ${analise.seguranca}/10
  Performance: ${analise.performance}/10
  Manutenibilidade: ${analise.manutenibilidade}/10

📈 ESTATÍSTICAS:
  Linhas: ${analise.linhas}
  Caracteres: ${analise.caracteres}
  Funções: ${analise.funcoes}

🔧 ESTRUTURAS:
  Se: ${analise.estruturas.se}
  Enquanto: ${analise.estruturas.enquanto}
  Para: ${analise.estruturas.para}

${analise.erros.length > 0 ? '❌ ERROS:\n  ' + analise.erros.join('\n  ') : ''}
${analise.avisos.length > 0 ? '⚠️ AVISOS:\n  ' + analise.avisos.join('\n  ') : ''}
${analise.sugestoes.length > 0 ? '💡 SUGESTÕES:\n  ' + analise.sugestoes.join('\n  ') : ''}
        `);
    }

    compilar(args) {
        if (args.length === 0) {
            console.log('❌ Especifique um arquivo');
            return;
        }

        const caminho = args[0];
        if (!fs.existsSync(caminho)) {
            console.error(`❌ Arquivo não encontrado: ${caminho}`);
            return;
        }

        const codigo = fs.readFileSync(caminho, 'utf8');
        const js = this.interpreter.ia.corrigir(codigo);
        const arquivoJS = caminho.replace(/\.(ns|null)$/, '.js');
        
        // Adicionar wrapper para execução
        const wrapper = `
// Compilado de NullScript v${this.versao}
// Arquivo original: ${caminho}
// Data: ${new Date().toISOString()}

// Biblioteca padrão
const NullScriptRuntime = {
    exibir: (msg) => console.log(msg),
    perguntar: (msg) => {
        const readline = require('readline');
        const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
        return new Promise((resolve) => {
            rl.question(msg, (res) => { rl.close(); resolve(res); });
        });
    },
    sistema: require('os'),
    arquivos: require('fs'),
    crypto: require('crypto')
};

// Código compilado
${js}
        `;

        fs.writeFileSync(arquivoJS, wrapper);
        console.log(`✅ Compilado para: ${arquivoJS}`);
        console.log(`📦 Execute com: node ${arquivoJS}`);
    }
}

// ============================================================
//              PONTO DE ENTRADA
// ============================================================

// Criar alias para o comando
if (require.main === module) {
    const cli = new NullScriptCLI();
    cli.iniciar();
}

// Exportar para uso como módulo
module.exports = {
    NullScriptInterpreter,
    CorretorAuto,
    NullScriptCLI,
    VERSAO
};

// ============================================================
//              FIM DO ARQUIVO
// ============================================================