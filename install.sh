#!/usr/bin/env sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
INSTALL_ROOT="${XDG_DATA_HOME:-$HOME/.local/share}/git-herd"
BIN_DIR="${HOME}/.local/bin"
TARGET_ROOT="$INSTALL_ROOT/current"
TARGET_SCRIPT="$BIN_DIR/git-herd"

mkdir -p "$TARGET_ROOT/src" "$BIN_DIR"

rm -rf "$TARGET_ROOT/src/git_herd"
cp -R "$SCRIPT_DIR/src/git_herd" "$TARGET_ROOT/src/git_herd"

cat >"$TARGET_SCRIPT" <<EOF
#!/usr/bin/env sh
set -eu
export PYTHONPATH="$TARGET_ROOT/src"
exec python3 -m git_herd "\$@"
EOF

chmod 755 "$TARGET_SCRIPT"

printf 'Installed git-herd to %s\n' "$TARGET_SCRIPT"

case ":$PATH:" in
    *":$BIN_DIR:"*)
        ;;
    *)
        printf 'Add %s to PATH to run git-herd directly.\n' "$BIN_DIR"
        ;;
esac
