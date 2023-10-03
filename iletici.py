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

async def main():
    yasakli_kelimeler = await yasakli_kelimeleri_oku()

    # Telethon ile oturum aç
    async with TelegramClient('session_name', api_id, api_hash) as client:
        # Kullanıcının sohbet listesini al
        dialogs = await client.get_dialogs()

        # Kullanıcıya sohbetleri göster
        print("Sohbet Listesi:")
        for i, dialog in enumerate(dialogs, 1):
            print(f"{i}. {dialog.name}")

        # Kullanıcıdan kaynak ve hedef sohbetleri seçmesini iste
        kaynak_sohbet_num = int(input("Kaynak sohbeti seçin (numara ile): "))
        hedef_sohbet_num = int(input("Hedef sohbeti seçin (numara ile): "))

        # Kaynak ve hedef sohbetleri belirle
        kaynak_sohbet = dialogs[kaynak_sohbet_num - 1]
        hedef_sohbet = dialogs[hedef_sohbet_num - 1]

        print(f"Kaynak sohbet: {kaynak_sohbet.name}")
        print(f"Hedef sohbet: {hedef_sohbet.name}")

        # Yeni mesajları izle
        @client.on(events.NewMessage(chats=[kaynak_sohbet]))
        async def handle_new_message(event):
            mesaj = event.message
            mesaj_metni = mesaj.text.lower()  # Mesajı küçük harf olarak alın

            # Yasaklı kelimeleri kontrol et
            for yasakli_kelime in yasakli_kelimeler:
                if yasakli_kelime in mesaj_metni:
                    print(f"❗Yasaklı kelime tespit edildi: {yasakli_kelime}")
                    return  # Yasaklı kelime bulunursa mesajı iletme

            # Yasaklı kelime bulunmadıysa mesajı ilet
            await client.send_message(hedef_sohbet, mesaj)

        # Mesajları izlemek için başla
        await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
    