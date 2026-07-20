SHELL := /bin/bash
GEN1 := Gen1
DIST := dist
CHAPTERS := $(wildcard $(GEN1)/*-*/??-chapter.md)
PDFS := $(patsubst $(GEN1)/%-chapter.md,$(DIST)/%-chapter.pdf,$(CHAPTERS))
HTMLS := $(patsubst $(GEN1)/%-chapter.md,$(DIST)/%-chapter.html,$(CHAPTERS))

.PHONY: all pdf html clean lint check-links

all: pdf html

$(DIST)/%-chapter.pdf: $(GEN1)/%-chapter.md
	@mkdir -p $(dir $@)
	@if command -v pandoc >/dev/null 2>&1; then \
		pandoc "$<" -o "$@" --pdf-engine=xelatex -V geometry:margin=2.5cm; \
	else \
		echo "Ошибка: pandoc не установлен. Установите: https://pandoc.org/installing.html"; \
		exit 1; \
	fi

$(DIST)/%-chapter.html: $(GEN1)/%-chapter.md
	@mkdir -p $(dir $@)
	@if command -v pandoc >/dev/null 2>&1; then \
		pandoc "$<" -o "$@" --standalone --toc; \
	else \
		echo "Ошибка: pandoc не установлен. Установите: https://pandoc.org/installing.html"; \
		exit 1; \
	fi

pdf: $(PDFS)

html: $(HTMLS)

clean:
	rm -rf $(DIST)

lint:
	@if command -v markdownlint-cli2 >/dev/null 2>&1; then \
		markdownlint-cli2 'Gen1/**/*.md' 'templates/**/*.md' 'prompts/**/*.md' 'examples/**/*.md' '*.md'; \
	else \
		echo "Ошибка: markdownlint-cli2 не установлен. Установите: npm install -g markdownlint-cli2"; \
		exit 1; \
	fi

check-links:
	@if command -v lychee >/dev/null 2>&1; then \
		lychee --no-progress 'Gen1/**/*.md' 'templates/**/*.md' 'prompts/**/*.md' 'examples/**/*.md' '*.md'; \
	else \
		echo "Ошибка: lychee не установлен. См. https://lychee.cli.rs"; \
		exit 1; \
	fi
