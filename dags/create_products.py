import pandas as pd
import random
import string

def create_products_data(path):
    """Function create products data for use in DAG"""
    columns = ["product_id", "product_name", "category", "price"]
    df = pd.DataFrame(columns=columns)

    product_id = 1
    category_data = ["notebook", "monitor" ,"keyboard", "mouse", "headset", "chair", "desk", "controller"]

    while product_id < 1000:
        category = random.choice(category_data)
        letters = string.ascii_letters
        
        #Notebook
        if category == "notebook":
            price = float(random.randrange(20000, 150000, 5000))
            product = ["Evo Pro", "NovaFlight", "Atlas", "Lumina Canvas" ,"SwiftX", "Zenith", "Aeris Lite", "VoltBook", "Strata X", "Muse", "Apex Gamer", "Nomad Pro", "StudioCraft", "BizLine", "Comet", "SpectraMax", "TitanCore", "VersaFlex", "Nimbus Touch", "EdgeLight"]
            model = f"{random.randrange(1,99)}{random.choice(letters).upper()}{random.randrange(1000,9999)}"
            product_name = f"{random.choice(product)} {model}"
            
        #Monitor
        if category == "monitor":
            price = float(random.randrange(3000, 20000, 500))
            product = ["VividView", "VividView", "SpectraMax Pro", "ChromeVision", "FlexView", "VisuGen VX", "LuminaLite", "Zenith Z-Curve", "AeroStream AS", " NovaSight NS", "Canvas Pro", "EyeFeast", "Paniramic View", "ClarityPrime", "FocusZone"]
            size = ["22-inch", "24-inch", "27-inch", "32-inch", "34-inch", "43-inch", "49-inch", "55-inch"]
            product_name = f"{random.choice(product)} {random.choice(size)}"
        
        #Gamming Gear
        gaming_gear_data = ["Apex Legion", "Cybernetic Forge", "Fractured Focus", "Havoc Labs", "Hyperweave Tech", "Mnemonic Gear", "Phantom Strike", "Quantum Flux", "Ragnarok Industries", "Renegade Collective", "Spectral Edge", "Tempestuous Tech", "Titanforged", "Valhalla Gear", "Wraithspire"]
        gaming_gear_brand = random.choice(gaming_gear_data)
        
        #Keyboard
        if category == "keyboard":
            price = float(random.randrange(1000, 10000, 500))
            model = [f"{random.choice(letters).upper()}{random.randrange(1,9)}", "Kinesis", "Onslaught", "Wraith", "TKL", "Whisper", "Eclipse", "CTRL", "Storm", "Shift", "Ghost", "Bifrost", "Elite"]
            product_name = f"{gaming_gear_brand} {random.choice(model)} Keyboard"

        #Mouse
        if category == "mouse":
            price = float(random.randrange(1000, 8000, 500))
            model = [f"{random.choice(letters).upper()}{random.randrange(1,9)}", "Viper", "Cobra", "Basilisk", "Leviathan", "Kraken", "Shadow", "Premium", "Elit", "Gamming", "Pro"]
            product_name = f"{gaming_gear_brand} {random.choice(model)} Mouse"
        
        #Headset
        if category == "headset":
            price = float(random.randrange(500, 5000, 250))
            model = [f"{random.choice(letters).upper()}{random.randrange(1,9)}", f"{random.choice(letters).upper()}{random.randrange(100,1500,100)}", f"{random.choice(letters).upper()}{random.randrange(10,100,10)}", "Aegis", "Echelon", "Tempest", "Synapse", "Eecall", "Umbra", "Q-Link", "Wireless", "Elite", "Pro", "Surround", "Audio", "ANC"]
            product_name = f"{gaming_gear_brand} {random.choice(model)} Headset"
            
        #Chair
        if category == "chair":
            price = float(random.randrange(500, 10000, 500))
            model = [f"{random.choice(letters).upper()}{random.randrange(1,9)}", f"{random.choice(letters).upper()}{random.randrange(100,1500,100)}", f"{random.choice(letters).upper()}{random.randrange(10,100,10)}", "Economic", "Embrace", "Cuddle", "Gaming", "Aero", "Premium", "Collection", "Collective", "Nexus", "Throne", "Prime", "Elite", "Pro", "Lumbar"]
            product_name = f"{gaming_gear_brand} {random.choice(model)} Chair"
            
        #Desk
        if category == "desk":
            price = float(random.randrange(500, 10000, 500))
            model = [f"{random.choice(letters).upper()}{random.randrange(1,9)}", f"{random.choice(letters).upper()}{random.randrange(100,1500,100)}", f"{random.choice(letters).upper()}{random.randrange(10,100,10)}", "Economic", "Embrace", "Cuddle", "Gaming", "Aero", "Premium", "Collection", "Collective", "Nexus", "Throne", "Prime", "Elite", "Pro", "Lumbar"]
            size = [100, 120, 140, 160, 170, 180, 200, 220, 240]
            product_name = f"{gaming_gear_brand} {random.choice(model)} {random.choice(size)} Desk"
            
        #Controler
        if category == "controller":
            price = float(random.randrange(500, 5000, 100))
            model = [f"{random.choice(letters).upper()}{random.randrange(1,9)}", f"{random.choice(letters).upper()}{random.randrange(100,1500,100)}", f"{random.choice(letters).upper()}{random.randrange(10,100,10)}"]
            product_name = f"{gaming_gear_brand} {random.choice(model)} Controller"
        
        data = {
            "product_id": [product_id],
            "product_name": [product_name],
            "category": [category],
            "price": [price]
        }
        
        new_df = pd.DataFrame(data)
        df = pd.concat([df,new_df], ignore_index=True)
        product_id +=1
    
    # df.to_csv(f'{path}/products.csv', index=False)
    return df
