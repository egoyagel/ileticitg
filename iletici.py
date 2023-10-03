from telethon.sync import TelegramClient, events
import asyncio

# API kimlik bilgileri
api_id = '29938408'
api_hash = '72e678f4d0476a433654320b5f895c28'

async def yasakli_kelimeleri_oku():
    try:
        with open('yasakli.txt', 'r', encoding='utf-8') as file:
            yasakli_kelimeler = file.read().splitlines()
            return yasakli_kelimeler
    except FileNotFoundError:
        return []

async def kaynak_sayisi_al():
    try:
        kaynak_sayisi = int(input("Kaç adet kaynak sohbet seçmek istersiniz: "))
        return kaynak_sayisi
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
        return await kaynak_sayisi_al()

async def kaynak_sohbet_sec(client):
    dialogs = await client.get_dialogs()
    print("Sohbet Listesi:")
    for i, dialog in enumerate(dialogs, 1):
        print(f"{i}. {dialog.name}")

    kaynaklar = []
    kaynak_sayisi = await kaynak_sayisi_al()

    for i in range(kaynak_sayisi):
        kaynak_sohbet_num = int(input(f"{i + 1}. kaynak sohbeti seçin (numara ile): "))
        kaynak_sohbet = dialogs[kaynak_sohbet_num - 1]
        kaynaklar.append(kaynak_sohbet)

    return kaynaklar

async def main():
    yasakli_kelimeler = await yasakli_kelimeleri_oku()

    # Telethon ile oturum aç
    async with TelegramClient('session_name', api_id, api_hash) as client:
        dialogs = await client.get_dialogs()
        kaynaklar = await kaynak_sohbet_sec(client)

        hedef_sohbet_num = int(input("Hedef sohbeti seçin (numara ile): "))
        hedef_sohbet = dialogs[hedef_sohbet_num - 1]

        print(f"Hedef sohbet: {hedef_sohbet.name}")

        # Yeni mesajları izle
        @client.on(events.NewMessage(chats=kaynaklar))
        async def handle_new_message(event):
            mesaj = event.message
            mesaj_metni = mesaj.text.lower()  # Mesajı küçük harf olarak alın

            # Yasaklı kelimeleri kontrol et
            for yasakli_kelime in yasakli_kelimeler:
                if yasakli_kelime in mesaj_metni:
                    print(f"Yasaklı kelime tespit edildi: {yasakli_kelime} (Kaynak: {event.chat.title})")
                    return  # Yasaklı kelime bulunursa mesajı iletme

            # Yasaklı kelime bulunmadıysa mesajı hedef sohbete ileterek çalışır
            await client.send_message(hedef_sohbet, mesaj)

        # Mesajları izlemek için başla
        await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
    