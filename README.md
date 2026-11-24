# Portfólio de Cauê Crillanovick

Site pessoal de desenvolvedor mobile com foco em iOS e AI builder: apps na App Store, IA usada com critério e ferramentas internas que destravam processos.

Site · 2026 · [cauecarneiro.github.io/portfolio](https://cauecarneiro.github.io/portfolio/)

## O que faz

- Página principal com os cinco apps na App Store, os apps de uso pessoal, a IA dentro dos apps, as ferramentas internas e as automações.
- Uma página interna por projeto, no mesmo molde: problema, meu papel, resultado e stack, com telas e vídeos.
- Página com os modelos de prompt que eu uso com os agentes de IA.
- Currículo em PDF para baixar.

## Meu papel

Projeto solo: conteúdo, design e código.

## Como foi feito

- `index.html` é o trecho-fonte da página principal (também usado no artefato do Claude).
- `paginas.py` gera as páginas internas a partir de dados em Python, reaproveitando o CSS da página principal.
- `./build.sh` gera tudo em `docs/`, que é o que o GitHub Pages publica (branch `main`, pasta `/docs`).
- Imagens e vídeos ficam em `docs/assets/`, com caminho relativo:
  - `apps/`: telas e ícones dos apps, as mesmas da App Store.
  - `perity/`, `racha/` e `teleprompter/`: telas tiradas no simulador e no Mac, sempre com dados de exemplo.
  - `ia/` e `ferramentas/`: telas das automações e ferramentas, com dados de exemplo e nomes genéricos.
- Visual em preto, branco e cinza, com azul puro como único acento. Animações com GSAP e ScrollTrigger por CDN, respeitando "reduzir movimento".

Não entram: telefone, contas, chaves, dados reais de banco ou de saúde, finanças e assuntos pessoais além da seção "fora do código".

## Tecnologias

HTML, CSS e JavaScript sem etapa de build, GSAP, Python para gerar as páginas internas.

## Como rodar

```sh
./build.sh
cd docs && python3 -m http.server 8791
```

Depois abra `http://127.0.0.1:8791/`.

---
Feito por Cauê Crillanovick · [portfólio](https://cauecarneiro.github.io/portfolio/) · [LinkedIn](https://www.linkedin.com/in/cau%C3%AA-carneiro)
