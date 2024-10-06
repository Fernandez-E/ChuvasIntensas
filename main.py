from functions.separacao import separador_variaveis

from datetime import datetime, timedelta

linhas, datas, horarios, precipitacao, eventos = [], [], [], [], []

with open('serra9900.txt', 'r') as arquivo:
    for linha in arquivo:
        linhas.append(linha.strip().replace('""', ' ').replace('"', ''))

    for item in linhas:
        datas.append(item[0:10])
        horarios.append(item[11:19])
        precipitacao.append(float(item[-6:]))

    i=0
    for i in range(len(datas)):
        eventos.append((datetime.strptime(f'{datas[i]} {horarios[i]}', "%m/%d/%Y %H:%M:%S"), precipitacao[i]))
        i+=1

chuvas_intensas = []
c_intensas = 1
data_inicio = eventos[0][0]
i=0
for i in range(1, len(eventos)):
    diff_tempo = eventos[i][0] - data_inicio

    if diff_tempo <= timedelta(hours=6):
        c_intensas+=1

    else:
        if c_intensas >= 40:
            chuvas_intensas.append((data_inicio, eventos[i - 1][0], c_intensas))
            print(f'{data_inicio} a {eventos[i - 1][0]}: Evento erosivo: {c_intensas} basculas ({c_intensas*0.25}mm)')
        else:
            print(f'{data_inicio}: {c_intensas} basculas')

        c_intensas = 1  # Reinicia a contagem
        data_inicio = eventos[i][0]  # Define o novo ponto de início

if c_intensas >= 40:
    print(f'{data_inicio} a {eventos[-1][0]}: Evento erosivo: {c_intensas} basculas')
else:
    print(f'{data_inicio}: {c_intensas} basculas')

print(f' CHUVAS INTENSAS: {chuvas_intensas}')


chuveros = open('serra9900-chuveros.txt', 'w')

i=0
c=0
for chuva in chuvas_intensas:
    chuveros.write(f'{chuva[0].day:02}/{chuva[0].month:02}/{chuva[0].year%100:02}\n')
    chuveros.write(f'{i+1} {chuva[2]} {chuva[0].hour:02} {chuva[0].minute:02} 0.0\n')
    for evento in eventos:
        if evento[0] >= chuva[0] and evento[0] <= chuva[1]:
            c+=1
            chuveros.write(f'{evento[0].hour:02} {evento[0].minute:02} 0.25\n')
    i+=1
chuveros.close()