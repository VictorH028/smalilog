```
❯ for lib in *.so; do
  if nm -D "$lib" 2>/dev/null | grep -qE 'obfs_check1_start|obfs_check1_finish'; then
    echo "[+] Found target: $lib"
    TARGET_LIBS+=("$lib")
  fi
done
```
