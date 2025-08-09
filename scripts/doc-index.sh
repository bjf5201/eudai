#!/bin/bash

set -e

# --- CONFIGURABLE PATHS

BASE_DIR="docs/adr"
INDEX_FILE="${BASE_DIR}/index.md"
DOCS=("docs/design.md" "README.md")

# Helper: Extract link text from ADR file (first non-empty line after the title)
extract_decision_title() {
    awk '
      /^# Decision -/ { found = 1; next }
      found && NF { print $0; exit }
    ' "$1"
}


# --- REGINERATE ADR INDEX
echo "Updating ADR index: ${INDEX_FILE}"

{
    echo "# Architecture Decision Records (ADRs)"
    echo ""
    find ${BASE_DIR} -type f -name "*.md" | sort | while read -r file; do
        DECISION_TITLE=$(extract_decision_title "${file}")
        # Fallback to filename if summary is missing
        if [[ -z "${DECISION_TITLE}" ]]; then
            DECISION_TITLE=$(basename "${file}" .md | sed 's/_/ /g')
        fi
        REL_PATH=${file#"${BASE_DIR}/"}
        echo "  - [${DECISION_TITLE}](${REL_PATH})"
    done
} > "${INDEX_FILE}"

echo "Updated ADR index at: ${INDEX_FILE}"

# --- UPDATE REFERENCES IN MAIN DOCS

for DOC in "${DOCS[@]}";do
    if [[ -f "${DOC}" ]]; then
        # Remove old ADR references by marker
        sed -i '/<!-- ADR_START -->/,/<!-- ADR_END -->/d' "${DOC}"
        # Insert new references
        {
            echo "<!-- ADR_START -->"
            echo "## Architecture Decision Records (ADRs)"
            tail -n +2 "${INDEX_FILE}"
            echo "<!-- ADR_END -->"
        } >> "${DOC}"
        echo "Updated ADR references in: ${DOC}"
    fi
done

echo "ADR index and main doc references updated."