# -*- coding: utf-8 -*-

def validar_ativo(Iq, par):
    try:
        ativos = Iq.get_all_open_time()
    except Exception as e:
        print(f"⚠ Erro ao obter ativos: {e}")
        return None

    try:
        if par in ativos["binary"] and ativos["binary"][par]["open"]:
            return par
    except:
        pass

    # fallback seguro
    try:
        if "-OTC" in par:
            normal = par.replace("-OTC", "")
            if normal in ativos["binary"] and ativos["binary"][normal]["open"]:
                print(f"🔁 Usando {normal}")
                return normal
        else:
            otc = par + "-OTC"
            if otc in ativos["binary"] and ativos["binary"][otc]["open"]:
                print(f"🔁 Usando {otc}")
                return otc
    except:
        pass

    return None