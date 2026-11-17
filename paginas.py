#!/usr/bin/env python3
"""Gera as páginas internas do portfólio (docs/<slug>.html) a partir dos dados abaixo.

Cada página reaproveita o CSS do index.html. Rodar pelo ./build.sh.
"""
import html
import os
import re

RAIZ = os.path.dirname(os.path.abspath(__file__))

SUB_CSS = """
.subbar{position:fixed;z-index:50;left:0;right:0;top:calc(env(safe-area-inset-top,0px) + 14px);display:flex;justify-content:space-between;gap:12px;padding-left:max(24px,var(--gl));padding-right:max(24px,var(--gr));pointer-events:none}
.subbar>*{pointer-events:auto}
.subbar svg{width:16px;height:16px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.top{padding-top:clamp(120px,16vw,190px);padding-bottom:clamp(36px,5vw,60px)}
.h1{font-size:clamp(2.8rem,8vw,6.4rem);letter-spacing:-.03em;line-height:.95;font-weight:500;margin:0;max-width:14ch}
.top .sub{font-size:clamp(1.1rem,1.6vw,1.3rem);max-width:58ch}
.ficha{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:22px;overflow:hidden;margin-top:clamp(36px,5vw,56px)}
.ficha>div{background:var(--black);padding:22px 22px 26px;min-width:0}
.ficha .lab{margin-bottom:8px}
.ficha p{color:var(--gray-2);font-size:.95rem;line-height:1.5}
@media(max-width:900px){.ficha{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.ficha{grid-template-columns:1fr}}
.bloco{padding-block:clamp(40px,6vw,80px)}
.bloco h2{font-size:clamp(1.8rem,3.6vw,3rem);max-width:22ch}
.bloco .txt{margin-top:22px;display:grid;gap:14px}
.bloco .txt p{color:var(--gray-2);max-width:68ch}
.bloco .list{margin-top:26px;max-width:860px}
.galeria{padding-block:clamp(8px,2vw,24px)}
.galeria .shots img,.galeria .shots video{height:clamp(420px,52vw,620px)}
.prox{display:flex;justify-content:flex-end;flex-wrap:wrap;gap:12px;padding:clamp(40px,6vw,80px) 0}
.bloco .pipe{grid-template-columns:repeat(var(--n,5),minmax(0,1fr))}
.bloco .step::before{background:var(--blue);border-color:var(--blue-soft)}
.bloco .pipe .fill{transform:none}
@media(max-width:860px){.bloco .pipe{grid-template-columns:1fr}}
.nota{font-size:.86rem;color:var(--gray);margin-top:18px;max-width:70ch}
"""

SETA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'


def e(t):
    return html.escape(t, quote=True)


def celulares(itens, rotulo):
    """itens: lista de (arquivo, alt) ou ('video', mp4, capa, alt)."""
    out = [f'<div class="shots" aria-label="{e(rotulo)}">']
    for it in itens:
        if it[0] == "video":
            _, mp4, capa, alt = it
            out.append(
                f'<div class="vid"><video muted loop playsinline preload="none" poster="{capa}" aria-label="{e(alt)}">'
                f'<source src="{mp4}" type="video/mp4"></video></div>'
            )
        else:
            arq, alt = it
            out.append(
                f'<button type="button" data-full="{arq}"><img src="{arq}" alt="{e(alt)}" loading="lazy"></button>'
            )
    out.append("</div>")
    return "\n".join(out)


def figura(arq, alt, legenda, w=1440, h=900):
    return (
        f'<figure class="fig"><button type="button" data-full="{arq}"><img src="{arq}" width="{w}" height="{h}" '
        f'alt="{e(alt)}" loading="lazy"></button><figcaption>{legenda}</figcaption></figure>'
    )


def passos(lista):
    n = len(lista)
    s = [f'<div class="pipe" style="--n:{n}" aria-label="Fluxo"><div class="fill"></div>']
    for t, p in lista:
        s.append(f'<div class="step on"><h4>{t}</h4><p>{p}</p></div>')
    s.append("</div>")
    return "".join(s)


def bloco(titulo, paragrafos=(), lista=(), extra="", alt=False):
    s = [f'<section class="bloco{" alt" if alt else ""}"><div class="w"><h2>{titulo}</h2>']
    if paragrafos:
        s.append('<div class="txt">' + "".join(f"<p>{p}</p>" for p in paragrafos) + "</div>")
    if lista:
        s.append('<ul class="list">' + "".join(f"<li><b>{a}</b> {b}</li>" for a, b in lista) + "</ul>")
    s.append(extra)
    s.append("</div></section>")
    return "".join(s)


P = []  # páginas

# ───────────────────────────── apps ─────────────────────────────
P.append(dict(
    slug="racha", secao="mais-apps", tipo="app multiplataforma · 2026", nome="Racha",
    resumo="Divide despesas em grupo e mostra quem paga a quem. Viagem, casa ou rolê: cada pessoa vê o próprio saldo e acerta por Pix, sem o app movimentar dinheiro.",
    links=[("página de apresentação", "https://landingpageracha.vercel.app")],
    ficha=[
        ("situação", "Versão 1.0 pronta no código desde 08/10/2026, com CI verde. Ainda não publicada nas lojas."),
        ("meu papel", "Produto e engenharia: defini as regras, a arquitetura e orquestrei os agentes de IA que escreveram o código, com teste e revisão em cada PR."),
        ("tamanho", "49 telas no app, 37 arquivos de teste no app e 39 no backend, 15 migrações de banco."),
        ("stack", "React Native com Expo, TypeScript, NestJS, PostgreSQL com TypeORM, Terraform na AWS."),
    ],
    corpo=[
        '<section class="galeria"><div class="w">' + celulares([
            ("video", "assets/racha/racha.mp4", "assets/racha/racha-capa.jpg", "Vídeo do Racha: início, grupos, despesa e acerto"),
            ("assets/racha/home.jpg", "Racha: início com saldos a receber e a pagar"),
            ("assets/racha/grupos.jpg", "Racha: lista de grupos"),
            ("assets/racha/grupo.jpg", "Racha: detalhe de um grupo de viagem"),
            ("assets/racha/despesa.jpg", "Racha: detalhe de uma despesa e a divisão"),
            ("assets/racha/nova.jpg", "Racha: nova despesa"),
            ("assets/racha/acertar.jpg", "Racha: acertar contas"),
            ("assets/racha/atividade.jpg", "Racha: atividade recente"),
            ("assets/racha/perfil.jpg", "Racha: perfil e chaves Pix"),
            ("assets/racha/boasvindas.jpg", "Racha: boas-vindas"),
            ("assets/racha/entrar.jpg", "Racha: tela de entrada"),
        ], "Telas do Racha") + '<p class="nota">Telas tiradas do app rodando no simulador, com um grupo de exemplo. As pessoas e os valores são fictícios.</p></div></section>',
        bloco("o que o app faz", lista=[
            ("Grupos.", "Viagem, casa, evento ou outro, com convite por código, por link ou por @usuário."),
            ("Despesas.", "Divisão igual, por valor fixo, por percentual ou por cotas, com categoria, local e recibo em foto."),
            ("Saldos.", "Cada pessoa vê quanto tem a receber e a pagar. O app simplifica as dívidas para reduzir o número de acertos."),
            ("Acerto.", "Mostra a chave Pix de quem recebe e registra o pagamento, total ou parcial. O app não movimenta dinheiro."),
            ("Avisos.", "Feed de atividade, notificações e lembrete de prazo de dívida."),
        ], alt=True),
        bloco("como foi construído", [
            "São três repositórios: o app, a API e a infraestrutura. O app conversa com a API por um contrato estável, e toda lacuna de API se resolve no backend, não com remendo no app.",
            "A API tem um módulo por domínio: autenticação, usuários, grupos, convites, despesas, pagamentos, notificações e envio de arquivos. O cálculo de saldo e a simplificação de dívidas são funções puras, testadas à parte. Dinheiro é sempre guardado em centavos.",
        ], lista=[
            ("Prova antes do merge.", "Tipos, lint, formatação e testes precisam passar. O CI também confere se o esquema do banco bate com as migrações."),
            ("Segurança.", "Sessão guardada no cofre do aparelho, login com Apple, limite de tentativas na autenticação e exclusão de conta pelo próprio usuário."),
            ("Entrada de desenvolvimento.", "Existe um atalho de login só para testes, e a API se recusa a subir em produção com ele ligado."),
        ]),
        '<section class="bloco alt"><div class="w"><h2>a página de apresentação</h2>' + figura("assets/racha/landing.jpg", "Página de apresentação do Racha", "A página que apresenta o app, também feita por mim.", 1440, 1100) + "</div></section>",
    ],
))

P.append(dict(
    slug="perity", secao="mais-apps", tipo="app para iPhone e Mac · 2026", nome="Perity",
    resumo="Controle financeiro pessoal: saldo, faturas, gastos do mês, contas fixas e investimentos, com dados de bancos reais por Open Finance e cada compra do Apple Pay registrada na hora.",
    links=[("código da versão aberta", "https://github.com/cauecarneiro/Perity-Comunidade")],
    ficha=[
        ("situação", "Uso pessoal no iPhone e no Mac desde 13/10/2026. A versão aberta está no GitHub, com licença MIT."),
        ("meu papel", "Projeto solo. Especifiquei, orquestrei os agentes de IA, revisei e medi o resultado."),
        ("tamanho", "Núcleo de regras em pacote Swift separado, com 184 testes."),
        ("stack", "SwiftUI, SwiftData, CloudKit, WidgetKit, App Intents, Keychain, Core Animation."),
    ],
    corpo=[
        '<section class="galeria"><div class="w">' + celulares([
            ("video", "assets/perity/perity.mp4", "assets/perity/perity-capa.jpg", "Vídeo do Perity: abertura animada e troca de abas"),
            ("assets/perity/ios-inicio.jpg", "Perity: início"),
            ("assets/perity/ios-investimentos.jpg", "Perity: investimentos comparados ao CDI"),
            ("assets/perity/ios-fixos.jpg", "Perity: contas fixas do mês"),
            ("assets/perity/ios-saude.jpg", "Perity: saúde financeira"),
            ("assets/perity/ios-analise.jpg", "Perity: gastos por categoria"),
        ], "Telas do Perity no iPhone") + '<p class="nota">Todas as telas mostram os dados de exemplo que vêm no app. Nenhum dado real aparece.</p></div></section>',
        '<section class="bloco alt"><div class="w"><h2>no Mac, outro conceito</h2><div class="txt"><p>No iPhone são três abas. No Mac o app é organizado como um caderno, com barra lateral de páginas, tabelas com contagem e soma e um ícone na barra de menus com o gasto do dia.</p></div><div class="figs">'
        + figura("assets/perity/mac-visaoGeral.jpg", "Perity no Mac: visão geral", "Visão geral.", 1440, 1050)
        + figura("assets/perity/mac-investimentos.jpg", "Perity no Mac: investimentos", "Investimentos e rendimento contra o CDI.", 1440, 1050)
        + figura("assets/perity/mac-gastos.jpg", "Perity no Mac: gastos do mês", "Gastos do mês por categoria.", 1440, 1050)
        + "</div></div></section>",
        bloco("decisões de engenharia", lista=[
            ("Somente leitura.", "O app lê os bancos por Open Finance e nunca move dinheiro. Não há engenharia reversa de aplicativo de banco."),
            ("Credenciais só no Keychain.", "Nada sensível fica em código, arquivo ou iCloud."),
            ("Dinheiro em centavos.", "Todo valor é inteiro, com sinal. As contas ficam num lugar só e as telas apenas mostram."),
            ("Sem contar duas vezes.", "Quando o banco confirma uma compra que o Apple Pay já tinha avisado, o app junta as duas."),
            ("Desempenho medido.", "A abertura caiu de cerca de 350 ms para 60 ms, medida com 1.937 lançamentos reais, antes e depois."),
            ("Sem servidor.", "Os dados ficam no aparelho e no iCloud privado de quem usa."),
        ]),
        bloco("plataforma Apple", lista=[
            ("Widgets", "no iPhone, no Mac e na tela de bloqueio."),
            ("Atalhos e Siri,", "com o registro automático de cada compra feita no Apple Pay."),
            ("Privacidade na tela:", "um toque oculta os valores, e a tela fica borrada na lista de apps recentes."),
            ("Importação", "de extratos em OFX e CSV para bancos fora do Open Finance."),
        ], alt=True),
    ],
))

P.append(dict(
    slug="teleprompter", secao="mais-apps", tipo="app para iPhone · código aberto · 2026", nome="Teleprompter",
    resumo="Cola o roteiro, aperta gravar e o texto rola enquanto a câmera filma. Sem conta, sem internet e sem assinatura. É o app que eu uso para gravar meus vídeos.",
    links=[("código", "https://github.com/cauecarneiro/Teleprompter")],
    ficha=[
        ("situação", "Em uso no meu iPhone desde 14/10/2026. Código aberto no GitHub."),
        ("meu papel", "Projeto solo, feito com agentes de IA a partir de um estudo de dez apps do mercado."),
        ("tamanho", "Núcleo em pacote Swift com 18 testes: leitura do roteiro, tempo e acompanhamento por voz."),
        ("stack", "SwiftUI, UIKit, AVFoundation, Speech, PhotoKit, XCTest, XcodeGen."),
    ],
    corpo=[
        '<section class="galeria"><div class="w">' + celulares([
            ("assets/teleprompter/tela-1.jpg", "Teleprompter: tela inicial"),
            ("assets/teleprompter/tela-2.jpg", "Teleprompter: editor com tempo por seção"),
            ("assets/teleprompter/tela-3.jpg", "Teleprompter: gravação com o texto rolando"),
        ], "Telas do Teleprompter") + "</div></section>",
        bloco("o que ele faz", lista=[
            ("Roteiro com seções.", "Linhas em caixa alta viram seções com atalho na tela de gravação. O que está entre parênteses aparece em cinza e fica fora da leitura."),
            ("Três modos de leitura.", "Automático, com velocidade em palavras por minuto, por voz ou manual."),
            ("Tempo sob controle.", "O editor mostra o tempo de cada seção e ajusta a velocidade para caber em 30, 45, 60 ou 90 segundos."),
            ("Gravação.", "Vertical, em 4K ou 1080p, sem filtro e sem recompressão. O arquivo original vai para a galeria."),
            ("Controles físicos.", "Botões de volume, Controle da Câmera, teclado ou controle Bluetooth."),
        ], alt=True),
        bloco("o que foi difícil", [
            "A leitura por voz usa o reconhecimento de fala do próprio aparelho, em português. O texto anda quando eu falo e espera quando eu improviso. Para isso o app alinha o que foi dito com o roteiro numa janela de palavras, com um algoritmo de alinhamento local.",
            "A rolagem do texto é feita em UIKit, a 120 Hz, dentro de um app SwiftUI, porque a rolagem declarativa não entregava a mesma suavidade. O texto fica no alto da tela, colado à câmera frontal, para o olhar não fugir da lente.",
            "Antes de dizer que salvou, o app confere se o vídeo tem áudio. Se uma ligação interromper a gravação, o take é salvo.",
        ]),
    ],
))

P.append(dict(
    slug="flag", secao="mais-apps", tipo="app para iPhone e Apple Watch · Challenge 17 · ago/2026", nome="Flag",
    resumo="Saúde da mulher. Em vez de só registrar ou prever o ciclo, o app mostra como a fase atual afeta o dia: sono, disposição e o treino recomendado.",
    links=[],
    ficha=[
        ("situação", "Desafio da Apple Developer Academy, desenvolvido de 10 a 28/08/2026. Não publicado."),
        ("meu papel", "Time de 4. Fiz a camada de domínio com as entidades e os modelos do HealthKit, o serviço de insights, o serviço de dicas de treino por fase e o modelo da tela de treino no iPhone."),
        ("arquitetura", "MVVM-C com fábrica de telas e injeção de dependência. A tela só desenha, o modelo fala com serviços, e só o serviço toca o HealthKit ou o banco."),
        ("stack", "SwiftUI, SwiftData, HealthKit, WatchConnectivity, WorkoutKit, complicações com WidgetKit."),
    ],
    corpo=[
        '<section class="galeria"><div class="w">' + celulares([
            ("assets/flag/home.jpg", "Flag: início com a fase do ciclo e o recado do dia"),
            ("assets/flag/ciclo.jpg", "Flag: ciclo com as quatro fases"),
            ("assets/flag/treino.jpg", "Flag: treino recomendado para a fase"),
        ], "Telas do Flag") + '<p class="nota">Telas tiradas do app rodando no simulador, com um ciclo de exemplo. Os cartões de sono e batimento aparecem vazios porque o simulador não tem dados do relógio.</p></div></section>',
        bloco("como funciona", lista=[
            ("Privacidade.", "Não há servidor nem conta. Tudo fica no aparelho."),
            ("HealthKit só para leitura.", "Frequência cardíaca, sono, temperatura e treinos vêm do HealthKit. O fluxo menstrual e o check-in do dia ficam no banco local do app, por decisão do time."),
            ("Apple Watch.", "O relógio tem app próprio, com check-in diário e complicação no mostrador, e sincroniza com o iPhone."),
            ("Fases.", "Menstrual, folicular, ovulação e lútea, cada uma com recado, dica e treino sugerido."),
        ], alt=True),
    ],
))

P.append(dict(
    slug="bubble", secao="mais-apps", tipo="app para Mac · Challenge 15 · jul/2026", nome="Bubble",
    resumo="Rotina para estudantes de medicina. Quando uma tarefa flexível não é cumprida, um motor realoca sozinho para o próximo horário livre, em vez de deixar o dia desmoronar. No código o projeto se chama Easy2Do.",
    links=[],
    ficha=[
        ("situação", "Desafio da Apple Developer Academy, entregue em 10/07/2026. Não publicado."),
        ("meu papel", "Time de 4. Trabalhei na tela de histórico de realocações e nas regras do motor, seguindo o documento de requisitos."),
        ("arquitetura", "MVVM em camadas: tela, modelo de tela, serviços e repositórios. O modelo de tela nunca toca o banco."),
        ("stack", "SwiftUI, SwiftData, @Observable, async/await. Funciona 100% offline."),
    ],
    corpo=[
        '<section class="bloco"><div class="w"><div class="figs">'
        + figura("assets/bubble/dia.jpg", "Bubble: linha do tempo do dia", "A linha do tempo do dia, com prioridade e categoria de cada tarefa.", 1600, 969)
        + figura("assets/bubble/resumo.jpg", "Bubble: resumo semanal", "O resumo semanal, com a distribuição por categoria.", 1600, 969)
        + figura("assets/bubble/tarefas.jpg", "Bubble: todas as tarefas", "Todas as tarefas da semana, com busca e filtro.", 1600, 969)
        + figura("assets/bubble/boasvindas.jpg", "Bubble: boas-vindas", "As boas-vindas, que montam a primeira rotina.", 1600, 969)
        + '</div><p class="nota">Telas tiradas do app rodando no Mac, com um dia de exemplo.</p></div></section>',
        bloco("o motor de realocação", [
            "O motor é Swift puro, sem interface, e recebe a hora atual como parâmetro, o que deixa cada regra testável. Ele roda de tempos em tempos e decide o que fazer com cada tarefa atrasada.",
        ], lista=[
            ("Prioridade.", "Alta, média e baixa têm pesos diferentes na hora de escolher quem ganha o próximo horário livre."),
            ("Regras por categoria.", "Estudos podem se empilhar no mesmo dia. Saúde e lazer não."),
            ("Permissão.", "Só é realocada a tarefa que a pessoa marcou como flexível."),
            ("Histórico.", "Cada realocação fica registrada e pode ser cancelada."),
        ], alt=True),
    ],
))

# ─────────────────────────── automações ───────────────────────────
P.append(dict(
    slug="carteiro", secao="automacoes", tipo="automação · desde 13/10/2026", nome="Carteiro",
    resumo="Um sistema de publicação em redes sociais com aprovação humana. Os rascunhos entram numa fila, eu aprovo na tela e o Carteiro publica no horário pelas APIs oficiais de LinkedIn, Threads, Instagram e X.",
    links=[],
    ficha=[
        ("resultado", "194 posts publicados em quatro redes até 17/11/2026 e 147,3 mil visualizações no Instagram e no Threads."),
        ("meu papel", "Idealizei e especifiquei o sistema e orquestrei os agentes que escreveram o código, com revisão e testes. Eu aprovo cada publicação."),
        ("qualidade", "268 casos de teste. Nada publica sem aprovação registrada, com o nome de quem aprovou."),
        ("stack", "TypeScript, Node, SQLite, página estática sem dependências, chaves no Chaveiro do macOS."),
    ],
    corpo=[
        '<section class="bloco"><div class="w">'
        + figura("assets/ia/carteiro-calendario.jpg", "Carteiro: calendário semanal com posts agendados", "O calendário da semana, com os horários de cada rede. Esta semana é uma demonstração montada com textos de posts meus já publicados.", 1440, 800)
        + '<div class="figs">'
        + figura("assets/ia/carteiro-aprovacao.jpg", "Carteiro: tela de aprovação de um post", "A aprovação: prévia do post como vai sair na rede, estado e notas. Também em modo de demonstração.", 1440, 960)
        + figura("assets/ia/carteiro-numeros.jpg", "Carteiro: painel de números", "Os números reais em 17/11/2026.", 1440, 960)
        + "</div></div></section>",
        bloco("como um post sai", extra=passos([
            ("Rascunho", "Um agente escreve a partir da pauta do dia e da minha voz."),
            ("Aprovação", "Eu leio a prévia, edito se quiser e aprovo na tela."),
            ("Agenda", "O post entra no próximo horário livre da grade daquela rede."),
            ("Publicação", "Sai pela API oficial da rede, com limite de tentativas."),
            ("Leitura", "Os números voltam para o painel e alimentam as próximas pautas."),
        ]), alt=True),
        bloco("cuidados de segurança", lista=[
            ("Aprovação assinada.", "Cada aprovação grava quem aprovou. Um agente nunca assina com o meu nome."),
            ("Chaves fora do código.", "Tokens e segredos ficam no Chaveiro do macOS. Nenhum vai para arquivo, log ou repositório."),
            ("Só APIs oficiais.", "Login por OAuth em cada rede, com renovação automática de acesso."),
            ("Arquivos servidos só na hora.", "Para as redes que buscam a mídia por endereço, o Carteiro abre um túnel temporário com caminho sorteado, só para os arquivos registrados, e fecha sozinho."),
        ]),
        '<section class="bloco alt" id="rotinas"><div class="w"><h2>as rotinas que rodam sozinhas</h2><div class="txt"><p>O Carteiro também mostra o que roda sem mim ao longo do dia: pesquisa de pautas, produção dos textos, varredura de comentários e conferência de que tudo rodou.</p></div>'
        + figura("assets/ia/carteiro-rotinas.jpg", "Carteiro: rotinas agendadas", "Cada rotina com horário, dono e próxima execução.", 1440, 960)
        + "</div></section>",
        '<section class="bloco" id="aprendizado"><div class="w"><h2>aprendizado das edições</h2><div class="txt"><p>Desde 01/11/2026 o sistema guarda o antes e o depois de cada texto que eu edito antes de aprovar. Um relatório diário mostra o que passou sem mexer, o que mudou palavra por palavra e o que eu reprovei.</p><p>O que se repete vira regra para os próximos rascunhos. Assim o texto que chega para aprovação fica cada vez mais parecido com o que eu escreveria.</p></div>'
        + passos([
            ("Rascunho", "O agente entrega o texto."),
            ("Edição", "Eu mudo o que não gostei."),
            ("Comparação", "O sistema guarda o antes e o depois."),
            ("Relatório", "Todo dia: o que passou, o que mudou, o que caiu."),
            ("Regra", "O padrão repetido entra no guia de voz."),
        ]) + "</div></section>",
        '<section class="bloco alt" id="comentarios"><div class="w"><h2>varredura de comentários</h2><div class="txt"><p>Todo dia, às 07h30, uma rotina acha os comentários sem resposta dos últimos dois dias no Instagram e no Threads e escreve rascunhos de resposta. Eu reviso e aprovo numa aba própria. Nenhuma resposta sai sozinha.</p></div>'
        + passos([
            ("07h30", "A rotina lê os comentários recentes."),
            ("Filtro", "Ficam só os sem resposta, dos últimos dois dias."),
            ("Rascunho", "Um agente escreve cada resposta."),
            ("Revisão", "Eu aprovo, edito ou descarto."),
        ]) + "</div></section>",
    ],
))

P.append(dict(
    slug="gatilho", secao="automacoes", tipo="automação · desde 19/10/2026", nome="Gatilho",
    resumo="Quando alguém comenta a palavra combinada num vídeo do Instagram, recebe uma mensagem privada com o material prometido. Roda sozinho, na nuvem, o tempo todo.",
    links=[],
    ficha=[
        ("o que resolve", "Entregar um material para cada pessoa que pede nos comentários, sem eu responder um por um."),
        ("meu papel", "Especifiquei o fluxo, as regras de entrega e os testes, e orquestrei os agentes que escreveram o código."),
        ("confiabilidade", "Recebe o aviso oficial da Meta e ainda confere a cada minuto, para não perder ninguém. Fila com prova de entrega."),
        ("stack", "Cloudflare Workers, banco D1, TypeScript, API oficial do Instagram."),
    ],
    corpo=[
        bloco("o caminho de um comentário", extra=passos([
            ("Comentário", "A pessoa comenta a palavra da campanha no vídeo."),
            ("Aviso", "A Meta avisa o serviço. Uma conferência a cada minuto cobre falhas do aviso."),
            ("Fila", "O pedido entra numa fila no banco, sem duplicar."),
            ("Mensagem", "A pessoa recebe uma mensagem privada com um botão."),
            ("Entrega", "Ao tocar no botão, recebe o material. A entrega fica registrada."),
        ])),
        bloco("o que deu trabalho", lista=[
            ("Não perder ninguém.", "Aviso em tempo real e conferência por minuto se complementam. A fila gira e tenta de novo quando a rede recusa."),
            ("Não mandar duas vezes.", "Cada comentário tem um registro único, e a entrega só conta quando a rede confirma."),
            ("Segredos.", "As chaves vão do Chaveiro do Mac direto para o cofre da Cloudflare, por um script que não mostra os valores."),
            ("Diagnóstico.", "Quando uma entrega atrasou, a causa foi achada pelo registro da fila e corrigida, e o passo a passo do diagnóstico ficou documentado."),
        ], alt=True),
    ],
))

P.append(dict(
    slug="carrossel", secao="automacoes", tipo="automação · desde 17/10/2026", nome="Gerador de carrossel",
    resumo="Do tema às lâminas prontas. Um agente pesquisa o assunto em várias fontes, outro escreve, e o sistema desenha as lâminas em código, no meu padrão visual, e manda para a fila de aprovação.",
    links=[],
    ficha=[
        ("o que resolve", "Fazer um carrossel com pesquisa, texto e desenho levava horas. Agora chega pronto para revisar."),
        ("meu papel", "Defini o padrão visual, os modelos de lâmina e as regras de fonte, e orquestrei os agentes."),
        ("regra", "Os números vêm com a fonte, e a lâmina mostra o trecho de onde saíram. Nada publica sem a minha aprovação."),
        ("stack", "HTML e CSS para as lâminas, Playwright para gerar as imagens, rotina agendada."),
    ],
    corpo=[
        '<section class="galeria"><div class="w">' + celulares(
            [(f"assets/ia/carrossel/0{i}.jpg", f"Lâmina {i} de 7 do carrossel") for i in range(1, 8)],
            "Lâminas de um carrossel gerado em código",
        ) + '<p class="nota">Um carrossel de sete lâminas gerado pelo sistema e publicado no meu perfil depois da aprovação.</p></div></section>',
        bloco("como funciona", extra=passos([
            ("Tema", "Vem da pesquisa de tendências do dia."),
            ("Pesquisa", "Um modelo mais forte busca dados e fontes."),
            ("Texto", "Outro modelo escreve no meu guia de voz."),
            ("Lâminas", "O sistema desenha em HTML e CSS e gera as imagens."),
            ("Aprovação", "O carrossel entra na fila do Carteiro."),
        ]), alt=True),
    ],
))

P.append(dict(
    slug="motor", secao="automacoes", tipo="automação · desde 05/10/2026", nome="Motor de edição",
    resumo="Edição de vídeo feita em código. Eu gravo, subo o arquivo e o motor corta os silêncios, coloca a legenda no meu padrão visual e trata o áudio. Um revisor confere cada vídeo antes de virar rascunho.",
    links=[],
    ficha=[
        ("o que resolve", "Editar cada vídeo à mão. Agora a edição roda de madrugada e eu só aprovo."),
        ("meu papel", "Defini o padrão visual, a cadeia de áudio e os critérios de revisão, e orquestrei os agentes."),
        ("áudio", "Redução de ruído, equalização, de-esser, compressor e normalização de volume, sempre na mesma ordem."),
        ("stack", "Remotion, TypeScript, DeepFilterNet, ffmpeg."),
    ],
    corpo=[
        '<section class="galeria"><div class="w">' + celulares([
            ("video", "assets/ia/motor-reel.mp4", "assets/ia/motor-reel-capa.jpg", "Trecho de um vídeo editado pelo motor, com corte e legenda automáticos"),
        ], "Vídeo editado pelo motor") + '<p class="nota">Trecho de um vídeo meu editado pelo motor: corte automático e legenda sincronizada com a fala. Toque no vídeo para ver os controles e ligar o som.</p></div></section>',
        bloco("as etapas", extra=passos([
            ("Entrada", "O vídeo bruto chega pela pasta combinada."),
            ("Transcrição", "A fala vira texto com o tempo de cada palavra."),
            ("Corte", "Silêncios e erros saem."),
            ("Montagem", "Legenda, inserções e ritmo seguem o padrão visual."),
            ("Áudio", "A cadeia padrão trata a voz."),
            ("Revisão", "Um revisor confere antes de virar rascunho."),
        ]), alt=True),
    ],
))

# ─────────────────────────── ferramentas ───────────────────────────
P.append(dict(
    slug="overview-painel", secao="ferramentas", tipo="ferramenta · código aberto · desde 08/10/2026", nome="Overview-Painel",
    resumo="Numa tela só: o que cada agente de IA está fazendo, quanto resta de cota em cada ferramenta, quais PRs estão abertos e o que depende de mim.",
    links=[("código", "https://github.com/cauecarneiro/Overview-Painel")],
    ficha=[
        ("gargalo removido", "Acompanhar vários agentes, cotas e PRs em terminais e sites diferentes, sem saber o que estava parado."),
        ("meu papel", "Projeto meu, de código aberto, com 14 estrelas e 4 forks no GitHub."),
        ("custo", "Nenhuma IA participa e nenhum token é gasto. O painel só lê."),
        ("stack", "Python, só com a biblioteca padrão, tmux e uma página estática."),
    ],
    corpo=[
        '<section class="bloco"><div class="w">' + figura("assets/ia/overview-painel.jpg", "Overview-Painel com treze agentes", "O painel com as telas de exemplo que acompanham o repositório.", 1440, 900) + "</div></section>",
        bloco("como funciona", lista=[
            ("Lê os terminais.", "Cada agente roda num terminal. O painel lê a tela de cada um e descobre se está trabalhando, ocioso ou esperando por mim."),
            ("Lê as cotas pela própria ferramenta.", "Claude Code, Codex e Antigravity informam quanto resta, sem gastar token."),
            ("Mostra o que depende de mim.", "PRs abertos, estado dos testes e pedidos de aprovação ficam numa lista só."),
            ("Fica na máquina.", "Nada escuta em porta pública e nada sai do computador. Há um modo de privacidade que esconde contas e e-mails."),
            ("Nunca inventa número.", "Terminal que não dá para ler aparece como sem leitura, com o motivo."),
        ], alt=True),
    ],
))

P.append(dict(
    slug="scrolling", secao="ferramentas", tipo="ferramenta · código aberto · desde 31/10/2026", nome="Scrolling",
    resumo="Extensão para Chrome e navegadores parecidos que tira um print da página inteira, do topo ao fim, em um clique. Se a página for gigante, divide a captura em várias imagens.",
    links=[("código", "https://github.com/cauecarneiro/scrolling")],
    ficha=[
        ("gargalo removido", "Capturar páginas longas à mão, em vários prints colados depois."),
        ("meu papel", "Projeto meu, de código aberto."),
        ("privacidade", "Não envia nada para a internet. O histórico das capturas fica só no navegador."),
        ("stack", "JavaScript puro, Manifest V3, sem etapa de build e sem dependências."),
    ],
    corpo=[
        '<section class="bloco"><div class="w">'
        + figura("assets/ferramentas/scrolling-resultado.jpg", "Scrolling: resultado de uma captura", "A tela de resultado: a página inteira capturada e já copiada para a área de transferência.", 1440, 888)
        + '<div class="figs">'
        + figura("assets/ferramentas/scrolling-opcoes.jpg", "Scrolling: opções", "As opções: formato, cópia automática e nome do arquivo.", 900, 995)
        + figura("assets/ferramentas/scrolling-popup.jpg", "Scrolling: janela da extensão durante a captura", "A janela da extensão durante a captura.", 648, 240)
        + "</div></div></section>",
        bloco("o que ela faz", lista=[
            ("Captura rolando e costurando.", "Funciona também quando quem rola é uma área interna da página, ou quando o conteúdo está dentro de outra página embutida."),
            ("Prepara a página.", "Desliga animações, carrega as imagens que só aparecem ao rolar e evita que menus fixos se repitam em cada fatia."),
            ("Páginas gigantes.", "Avisa e divide em duas ou mais imagens, em vez de travar."),
            ("Copia sozinha.", "A imagem vai para a área de transferência assim que a captura termina."),
            ("Arquivos.", "Histórico local com seleção, exclusão e download em lote, em PNG ou JPG."),
        ], alt=True),
    ],
))

P.append(dict(
    slug="life-track", secao="ferramentas", tipo="ferramenta · código aberto · desde 31/10/2026", nome="Life Track",
    resumo="Painel local de saúde e treino com os dados do relógio Garmin: sono, variabilidade cardíaca, estresse, treinos e um mapa de calor de 12 meses.",
    links=[("código", "https://github.com/cauecarneiro/life-track")],
    ficha=[
        ("gargalo removido", "Dados de saúde e treino espalhados nos apps do fabricante, sem uma visão única."),
        ("meu papel", "Projeto meu, de código aberto."),
        ("privacidade", "Não guarda nada em disco. Os dados ficam só na memória, por poucos minutos."),
        ("stack", "Python com FastAPI, JavaScript, API pessoal da Garmin."),
    ],
    corpo=[
        bloco("como funciona", extra=passos([
            ("Navegador", "Mostra os gráficos."),
            ("Servidor local", "Traduz os dados e guarda só em memória."),
            ("API do fabricante", "A chave nunca sai do servidor."),
        ])),
        bloco("o que o painel mostra", lista=[
            ("Resumo do dia", "em texto, escrito a partir dos números, com aviso quando o relógio não sincroniza."),
            ("Cada indicador", "com o dia no topo, a semana em gráfico próprio e as médias: sono, passos, estresse, calorias, frequência cardíaca e variabilidade."),
            ("Treinos", "com mapa, ritmo, frequência, altimetria, zonas e voltas, além do mapa de calor do ano."),
            ("Teclado e acessibilidade.", "Setas trocam de dia e de semana, há busca rápida e um estudo de usabilidade documentado no repositório."),
        ], alt=True),
        '<section class="bloco"><div class="w"><p class="nota">Esta página não tem imagens porque o painel só mostra os meus dados reais de saúde. O modo de demonstração com dados fictícios está no roteiro do projeto.</p></div></section>',
    ],
))

P.append(dict(
    slug="guarda-de-segredos", secao="ferramentas", tipo="ferramenta interna · desde 07/11/2026", nome="Guarda de segredos",
    resumo="Um porteiro que barra senha, token e chave antes de chegarem a um commit, um log, um documento ou um serviço externo. Roda nos ganchos dos agentes de IA e do git.",
    links=[],
    ficha=[
        ("gargalo removido", "O risco de uma credencial vazar quando vários agentes trabalham ao mesmo tempo no mesmo computador."),
        ("meu papel", "Defini a regra e os pontos de bloqueio."),
        ("como roda", "Local, sem IA e sem servidor. É uma conferência por padrão de texto, rápida e previsível."),
        ("stack", "Shell, ganchos do git e dos agentes."),
    ],
    corpo=[
        bloco("a regra", [
            "Usar pode, vazar não. Um agente pode usar uma chave para a tarefa que eu pedi, mas não pode guardar nem escrever o valor em lugar nenhum.",
        ], lista=[
            ("Antes do comando.", "O porteiro lê o que o agente vai executar ou escrever. Se houver cara de segredo, bloqueia e explica."),
            ("Antes do commit.", "O mesmo vale para o git, em qualquer repositório do computador."),
            ("Sem contorno.", "Um bloqueio não se contorna. O agente para e me avisa o que foi barrado."),
            ("No código, só o nome.", "A configuração guarda o nome da variável. O valor fica no cofre do sistema ou do serviço."),
        ]),
        bloco("os pontos de bloqueio", extra=passos([
            ("Agente", "Vai rodar um comando ou escrever um arquivo."),
            ("Porteiro", "Confere o conteúdo por padrões de segredo."),
            ("Passa", "Sem segredo, segue normal."),
            ("Barra", "Com segredo, bloqueia e diz o motivo."),
        ]), alt=True),
    ],
))

P.append(dict(
    slug="contexto", secao="ferramentas", tipo="ferramenta interna · desde out/2026", nome="Contexto",
    resumo="Cuida da memória de trabalho dos agentes de IA. Quando a janela de contexto de um agente enche, ele perde qualidade. Esta ferramenta mede, avisa e executa a limpeza ou o resumo na hora certa.",
    links=[],
    ficha=[
        ("gargalo removido", "Agentes perdiam qualidade e tempo quando a janela de contexto enchia, e alguém precisava vigiar."),
        ("meu papel", "Defini o protocolo: quando limpar, quando resumir e quando terminar a tarefa antes."),
        ("controle", "Tem chave de liga e desliga e um diário de cada ação."),
        ("stack", "Shell e ganchos do Claude Code."),
    ],
    corpo=[
        bloco("o protocolo", extra=passos([
            ("Medir", "A ferramenta acompanha quanto da janela cada agente já usou."),
            ("Decidir", "Trocou de tarefa: limpa. Tarefa longa e janela cheia: resume."),
            ("Executar", "O próprio agente pede e a ferramenta executa."),
            ("Registrar", "Cada ação vai para um diário."),
        ])),
        bloco("por que importa", [
            "Com muitos agentes em paralelo, o custo e a qualidade dependem de cada um trabalhar com o contexto certo. Um agente com a janela cheia erra mais e gasta mais.",
            "A regra nasceu de medição: limpar ao trocar de tarefa, resumir só com a janela entre 65% e 75% e trabalho ainda por fazer.",
        ], alt=True),
    ],
))


def render(p, css):
    links = "".join(
        f'<a class="pill sm{" solid" if i == 0 else ""}" href="{u}" target="_blank" rel="noopener">{e(t)}</a>'
        for i, (t, u) in enumerate(p["links"])
    )
    ficha = "".join(f'<div><span class="lab">{e(a)}</span><p>{b}</p></div>' for a, b in p["ficha"])
    i = [x["slug"] for x in P].index(p["slug"])
    prox = P[(i + 1) % len(P)]
    desc = re.sub(r"<[^>]+>", "", p["resumo"])
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#000000">
<title>{e(p["nome"])} · Cauê Crillanovick</title>
<meta name="description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600&family=Tinos:ital@1&display=swap">
<style>{css}{SUB_CSS}</style>
</head>
<body>
<div class="subbar">
  <a class="pill" id="voltar" href="index.html#{p["secao"]}">{SETA}voltar ao portfólio</a>
  <a class="pill solid" href="index.html#contato">falar comigo</a>
</div>
<main>
<section class="top"><div class="w">
  <span class="lab">{e(p["tipo"])}</span>
  <h1 class="h1">{e(p["nome"])}</h1>
  <p class="sub">{p["resumo"]}</p>
  {f'<div class="links">{links}</div>' if links else ''}
  <div class="ficha">{ficha}</div>
</div></section>
{"".join(p["corpo"])}
<div class="w"><nav class="prox" aria-label="Outras páginas">
  <a class="pill solid" href="{prox["slug"]}.html">a seguir: {e(prox["nome"])}</a>
</nav></div>
</main>
<footer><div class="w"><span>Cauê Crillanovick <span class="wm">cauenovic</span></span><span>Brasília, 2026</span></div></footer>
<dialog class="lb" id="lb" aria-label="Imagem ampliada"><img id="lbimg" alt=""></dialog>
<script>
(function(){{
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  /* voltar: retorna ao ponto exato da página principal quando a pessoa veio de lá */
  var voltar=document.getElementById("voltar");
  if(voltar){{
    var veioDoPortfolio=false;
    try{{ veioDoPortfolio=sessionStorage.getItem("pf-y")!==null; }}catch(err){{}}
    if(veioDoPortfolio) voltar.setAttribute("href","index.html");
  }}
  var lb=document.getElementById("lb"), lbimg=document.getElementById("lbimg");
  if(lb && typeof lb.showModal==="function"){{
    document.querySelectorAll("[data-full]").forEach(function(b){{
      b.addEventListener("click",function(){{ var im=b.querySelector("img"); lbimg.src=b.dataset.full; lbimg.alt=im?im.alt:""; lb.showModal(); }});
    }});
    lb.addEventListener("click",function(){{ lb.close(); }});
  }}
  document.querySelectorAll(".vid video").forEach(function(v){{
    v.addEventListener("click",function(){{ v.controls=true; v.muted=false; }});
    if(reduce || !("IntersectionObserver" in window)){{ v.controls=true; return; }}
    new IntersectionObserver(function(es){{ es.forEach(function(x){{ if(x.isIntersecting){{ var pr=v.play(); if(pr&&pr.catch) pr.catch(function(){{ v.controls=true; }}); }} else {{ v.pause(); }} }}); }},{{threshold:.4}}).observe(v);
  }});
}})();
</script>
</body>
</html>
"""


def main():
    fonte = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()
    css = re.search(r"<style>(.*?)</style>", fonte, re.S).group(1)
    for p in P:
        destino = os.path.join(RAIZ, "docs", p["slug"] + ".html")
        open(destino, "w", encoding="utf-8").write(render(p, css))
    print(f"{len(P)} páginas internas geradas")


if __name__ == "__main__":
    main()
