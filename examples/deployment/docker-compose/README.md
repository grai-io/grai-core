

```bash
docker volume create --driver local \
    --opt type=none \
    --opt device=/var/opt/my_website/dist \
    --opt o=bind grai-app
```
