# demotivator-bot

Простой Telegram-бот для создания демотиваторов с вашей вотермаркой.

Сделано за 24.06.2025 xDx

[dem_example.webm](https://github.com/user-attachments/assets/b9c7d34e-d6ad-43aa-8c0f-346a6018a196)

## Функционал
- [X] Создание демотиваторов
- [X] Возможность сделать бота приватным
- [ ] Возможность изменить размеры демотиватора
- [ ] Возможность получить оригинал демотиватора

## Использование

1. Установите [Docker](https://www.docker.com/)
2. Получите токен бота в [@BotFather](https://t.me/BotFather)
3. Загрузите нужный шрифт в нужную директорию (в нашем случае - `/host_path/to/font.ttf`)
4. 
```shell
docker run -d \
  -e ADMIN_IDS="[ADMIN_ID1, ADMIN_ID2]" \
  -e BOT_TOKEN="BOT_ID:SECRET_TOKEN" \
  -e FONT_PATH="/app/media/font.ttf" \
  -e WATERMARK="@ d 3 m 1 k _ b o t" \
  -e IS_PRIVATE="true" \
  -v "/host_path/to/font.ttf:/app/media/font.ttf" \
  ghcr.io/timtaran/demotivator-bot:latest
```
5. Всё!

### Переменные окружения
- `BOT_TOKEN` - Токен бота
- `WATERMARK` - Текст вотермарки (если вы хотите такую же как у KomaruDemik, то добавьте пробел после каждого символа)
- `FONT_PATH` - Путь к шрифту
- `IS_PRIVATE` - Является ли бот приватным
- `ADMIN_IDS` - ID админов в формате `[1, 2, 3, ...]` (сейчас - те, кому будет доступен приватный бот)
- `DEBUG_MODE` - Определяет будут ли выводится DEBUG логи

## Благодарности

- [KomaruDemikBot](https://t.me/KomaruDemik_bot) за вдохновение
- [nesclass](https://github.com/nesclass/) за реализацию [подобного бота](https://github.com/nesclass/demotivator-bot) и публикацию под MIT лицензией
- [Моей кошке](https://t.me/catsune_mewku) за то что прикольная
