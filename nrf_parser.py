from ruuvitag_sensor.decoder import Df5Decoder


#file_path="nrf_logging/Log 2023-07-06 19_40_38.txt"

def get_date(file):
    date=(file.readline()).rstrip('\n')
    date=date.split(', ')[1]
    
    return date

def get_MAC(input):
    mac = (input.readline()).rstrip('\n')
    if "Ruuvi 3750 " in mac:
        mac=mac.split("Ruuvi 3750 ")[1]
        mac=mac[1:-1]
        mac=mac.replace(":","")
        
    return mac


def read_lines(file_path):
    lines = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        creation_date=get_date(file)
        mac_address=get_MAC(file)  

        for line in file:
            out=[]
            line = line.rstrip('\n')  # Az LF karakter eltávolítása a sor végéről
            
            if "Notification received from " in line:
                
                line = line.split("(0x) ")
                
                out.append(creation_date+" "+line[0][2:10])
                out.append(line[1].replace("-","")+mac_address)

                lines.append(out)

    return lines

def parse_data(file_path):
   
    datain=read_lines(file_path)

    parsed=[]

    for data in datain:
        decoded = Df5Decoder().decode_data(data[1])
        decoded.update({"date": data[0]})
        
        parsed.append(decoded)
        
    return parsed


    




