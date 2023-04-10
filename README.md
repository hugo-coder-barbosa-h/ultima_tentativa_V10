# Bot Projeto de Lei 

O  bot  'Projeto de Lei' tem como objetivo informar, de maneira atualizada, quais Pls foram aprovados pela Câmara dos Deputados através da API da Câmara. 
O desenvolvimento do projeto faz parte do projeto final de Algoritmos de Automação do Master em Jornalismo de Dados, Automação e Data Storytelling do Insper.

O desenvolvimento do projeto faz parte do projeto final de Algoritmos de Automação do Master em Jornalismo de Dados, Automação e Data Storytelling do Insper.

As funcionalidades se baseiam na seguinte dinâmica: envio e recebimento de mensagens através da API da API do Telegram ( biblioteca requests e o método webhook via site Flask),  utilização de planilhas (Google Sheets) para guardar informações, no caso concreto os Projetos de Leis aprovados (biblioteca gspread) e envio dessas informações ao site final, via Render. 

Em suma: o interessado acessa o bot, consulta os Projetos de Lei aprovados em tempo real, podendo também acessar tais projetos pelo site para maiores detalhes e para uma melhor visualização.  



