Secret to set up Datadog API key:

```yaml
---
apiVersion: v1
kind: Secret
metadata:
  namespace: sales-prod
  name: datadog
type: Opaque
data:
  key: BASE64_ENCODED_KEY
```

To base64 encode API key, be careful of endlines.  Use this:

```
echo -n key1234 | base64
```

If you don't include the `-n`, you'll get extra endlines in your secret, and this will cause problems.

Example usage:

```bash
DD_API_KEY=abcdef1234 python3 app.py -i 5 -b 12 -n justin.metric -m 80 -a helloworld -e baseline
```

or

```bash
export DD_API_KEY=abcdef1234
python3 app.py \
    -n justin.metric \
    -m 80 \
    -a helloworld \
    -e baseline
```

Docker image:
```bash
docker run -it \
    -e DD_API_KEY=abcdef1234 \
    justinrlee/demo-datadog-app:latest \
        -n custom.metric \
        -m 123 \
        -e canary \
        -a demoapp
```