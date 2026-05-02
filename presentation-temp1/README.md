# Presentation TeX Structure

This directory is organized around `main.tex` as the canonical Beamer entry point.

## Layout

- `main.tex` - canonical presentation source.
- `enjoy-math-colloquium-260502.tex` - compatibility wrapper for the previous filename.
- `beamerthemeCodingTeal.sty`, `beamer*themeCodingTeal.sty` - thin Beamer discovery shims.
- `tex/` - shared preamble, title metadata, command definitions, listings, algorithms, and boxes.
- `theme/` - local `CodingTeal` Beamer theme implementation files.
- `chapters/` - active talk content.
- `tikzs/` - standalone TikZ source files and PDFs used as presentation graphics.
- `assets/` - non-TikZ presentation graphics.
- `archive/legacy-pages/` - older slide snippets that are not part of the current deck.
- `build/` - generated LaTeX byproducts and PDFs.

## Build

From this directory:

```sh
mkdir -p build
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

The previous entry-point name also works:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build enjoy-math-colloquium-260502.tex
```

No Word document is part of this TeX workflow.
