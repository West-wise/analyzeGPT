import sys
import struct
import binascii
import uuid

# GPT에서 맨 처음 512는 MBR과의 호환 용도

# 그럼 일단 512를 건너뛰고 읽어서 헤더부터 읽어내자
with open(sys.argv[1], 'rb') as f:
    
    # Sector0 = f.read(512)
    # f.seek(512)
    GPT_Header = f.read(1024)
    # 파일 시스템 타입을 읽기 위해 MBR + Header을 읽음
    f.seek(1024)
    # MBR + Header만큼 건너 뜀
    GPT_Sector = f.read(128 * 6)
    # MBR과 GPT 헤더를 건너뛰고 6개 엔트리를 읽어냄



#엔트리 수 만큼 반복하자
for i in range(6):
    entry = GPT_Sector[i * 128:(i + 1) * 128]
    
    # Partition Type GUID 읽어옴
    temp = entry[0:4][::-1] + entry[4:6][::-1] + entry[6:8][::-1] + entry[8:16]
    Type_guid = uuid.UUID(temp.hex())

    guid = uuid.UUID(entry[16:32].hex())
    Real_offset = struct.unpack('<Q', entry[32:40])[0] * 512
    f = open(sys.argv[1],'rb')
    f.seek(Real_offset+3)
    FST = f.read(8).decode()

    # Size를 올바르게 계산
    size = struct.unpack('<Q', entry[40:48])[0] - struct.unpack('<Q', entry[32:40])[0]

    entry_info = {
        "GUID": str(guid).upper(),
        "Partition Type GUID": str(Type_guid).upper(),
        "File System Type" : str(FST),
        "Real Offset":hex(Real_offset),
        "Size": size
    }
    print(entry_info)
