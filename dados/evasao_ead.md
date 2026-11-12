# Evasão em cursos a distância

Matrículas de uma plataforma de cursos de graduação a distância. Cada linha é uma
matrícula, com o engajamento do aluno no primeiro mês e a indicação de que ele evadiu
antes de concluir o primeiro ano.

- **Linhas:** 50.000
- **Colunas:** 15
- **Período:** matrículas de 01/01/2022 a 30/06/2025
- **Granularidade:** uma matrícula
- **Arquivo:** `evasao_ead.csv`, separado por vírgula, codificação UTF-8

Em fevereiro de 2024 a plataforma implantou a tutoria ativa, em que os tutores procuram os
alunos pelo fórum nas primeiras semanas do curso.

## Colunas

| coluna | descrição | unidade |
|---|---|---|
| `id_matricula` | identificador da matrícula | |
| `data_matricula` | data da matrícula | AAAA-MM-DD |
| `uf` | UF do aluno | |
| `area_curso` | área do curso: tecnologia, gestao, saude ou educacao | |
| `modalidade_ingresso` | forma de ingresso | |
| `turno_preferencial` | turno em que o aluno declarou estudar | |
| `possui_bolsa` | se o aluno tem bolsa de 50% (sim ou nao) | |
| `idade` | idade do aluno na matrícula | anos |
| `valor_mensalidade` | mensalidade paga | R$ |
| `num_acessos_30d` | acessos à plataforma nos primeiros 30 dias | |
| `tempo_plataforma_h_30d` | tempo na plataforma nos primeiros 30 dias | h |
| `num_atividades_entregues` | atividades entregues nos primeiros 30 dias, de 0 a 12 | |
| `nota_media_atividades` | nota média nas atividades entregues, de 0 a 10 | |
| `num_mensagens_forum` | mensagens no fórum nos primeiros 30 dias | |
| `evadiu` | 1 se o aluno evadiu no primeiro ano, 0 caso contrário | |
