import random
import math

# Definizione dei prod
dict_processori = {
    1: 'STM32F401',
    2: 'STM32H7',
    3: 'STM32N6',
}
dict_sensori = {
    1: 'LSM6DSO',
    2: 'LIS2DW12',
    3: 'LPS22HB',
}
dict_memorie = {
    1: 'M24C32-R',
    2: 'M24C32-F',
    3: 'M24C32-DF',
}

processori = list(dict_processori.values())  
sensori = list(dict_sensori.values())
memorie = list(dict_memorie.values())

def lotto_processori():
    qnt_prod = {prod: random.randint(1000, 10000) for prod in processori}
    return qnt_prod

def lotto_sensori():
    qnt_prod = {prod: random.randint(1000, 10000) for prod in sensori}
    return qnt_prod

def lotto_memorie():
    qnt_prod = {prod: random.randint(1000, 10000) for prod in memorie}
    return qnt_prod

def gen_prod(): 
    param_prod = {}
    hours_in_a_day = 24

    
    for prod in processori:
        # Capacità oraria casuale per ogni prod
        chips_per_hour = random.randint(1200, 3500) 
        # Tempo di produzione per unità in minuti 
        time_unit = round(60 / chips_per_hour, 5)  
        # Capacità massima giornaliera
        max_giorno = chips_per_hour * hours_in_a_day  
        param_prod[prod] = {
            'time_unit': time_unit,
            'max_giorno': max_giorno
        }
    for prod in sensori:
        chips_per_hour = random.randint(5000, 8000)  
        time_unit = round(60 / chips_per_hour, 5)  
        max_giorno = chips_per_hour * hours_in_a_day  
        param_prod[prod] = {
            'time_unit': time_unit,
            'max_giorno': max_giorno
        }
        
    for prod in memorie:
        chips_per_hour = random.randint(7000, 10000)  
        time_unit = round(60 / chips_per_hour, 5)  
        max_giorno = chips_per_hour * hours_in_a_day 
        param_prod[prod] = {
            'time_unit': time_unit,
            'max_giorno': max_giorno
        }

    return param_prod

def time_prod(qnt_prod, param_prod, max_all):
    time_total = 0
    work_day = 0

    qnt_rimanente = qnt_prod.copy()

     # Loop che continua finché ci sono ancora prod da produrre
    while any(qnt_rimanente.get(prod, 0) > 0 for prod in qnt_prod):
        work_day += 1
        tempo_giornata = 0
        left_d = max_all  

        # Produzione per giorno
        for prod in qnt_prod:
            if qnt_rimanente.get(prod, 0) > 0 and left_d > 0:
                qnt_to_prod = qnt_rimanente[prod]
                all_max_prod = param_prod[prod]['max_giorno']

                # Limita la produzione 
                left_today = min(all_max_prod, qnt_to_prod, left_d)

                # Assicurarsi che ci sia produzione
                if left_today > 0:  
                    time_unit = param_prod[prod]['time_unit']
                    tempo_giornata += left_today * time_unit
                    qnt_rimanente[prod] -= left_today
                    left_d -= left_today

        time_total += tempo_giornata  

    return time_total, work_day


def calcola_tempo_per_prod(qnt, time_unit, max_giorno):
    tempo_per_prod = 0
    qnt_rimanente = qnt

    # Calcoliamo quanto tempo ci vuole 
    while qnt_rimanente > 0:
        produzione_giornaliera = min(max_giorno, qnt_rimanente)
        tempo_per_prod += produzione_giornaliera * time_unit
        qnt_rimanente -= produzione_giornaliera

    return tempo_per_prod

def ore_minuti(tempo_in_ore):
    ore = int(tempo_in_ore)
    minuti = round((tempo_in_ore - ore) * 60)

    return f"{ore} ore e {minuti} minuti"

if __name__ == "__main__":
    # Simulazione del processo produttivo
    qnt_p = lotto_processori()
    qnt_s = lotto_sensori()
    qnt_m = lotto_memorie()
    param_prod = gen_prod()

    max_all = random.randint(1200, 3500) * 24

    tot = sum(qnt_p.values()) + sum(qnt_s.values()) + sum(qnt_m.values())
    for prod in processori:
        proporzione = qnt_p[prod] / tot
        param_prod[prod]['max_giorno'] = round(max_all * proporzione)

    for prod in sensori:
        proporzione = qnt_s[prod] / tot
        param_prod[prod]['max_giorno'] = round(max_all * proporzione)
    


    for prod in memorie:
        proporzione = qnt_m[prod] / tot
        param_prod[prod]['max_giorno'] = round(max_all * proporzione)

    time_total_p, w_day_p = time_prod(
        qnt_p, param_prod, max_all
    )

    time_total_s, w_day_s = time_prod(
        qnt_s, param_prod, max_all
    )
    time_total_m, w_day_m = time_prod(
        qnt_m, param_prod, max_all
    )

    time_t = time_total_p + time_total_s + time_total_m
    work_day = w_day_p + w_day_s + w_day_m

    print("\nQuantità da produrre per prod (processori):", qnt_p)
    print("\nQuantità da produrre per prod (sensori):", qnt_s)
    print("\nQuantità da produrre per prod (memorie):", qnt_m)
    print("Parametri produttivi per prod:")

    for prod, param in param_prod.items():    
        tempo_per_1000_unita_minuti = param['time_unit'] * 1000  
        # Tempo formattato in ore e minuti
        tempo_formattato = ore_minuti(tempo_per_1000_unita_minuti / 60)  
        print(f"  {prod}: Tempo per 1000 unità = {tempo_formattato}, "
            f"Capacità massima giornaliera = {param['max_giorno']} unità")
        
    print(f"\nCapacità complessiva giornaliera: {max_all} unità")

    # Conversione in minuti
    time_tot_prod = time_t / 60  

    print(f"Tempo totale di produzione: {ore_minuti(time_tot_prod)}")
    print(f"Giorni lavorativi necessari: {work_day} giorni")
