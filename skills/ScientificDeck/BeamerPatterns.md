# Beamer LaTeX Patterns

> Default style: Cunningham/Spina minimal (custom on default base). 1:1 from [ClaudeCodeTools/Presentations/main.tex](https://github.com/aspi6246/ClaudeCodeTools/blob/main/Presentations/main.tex).

## Complete Default Preamble

Every ScientificDeck presentation starts with this preamble. Copy verbatim, then add `\title`, `\author`, `\date`, and content.

```latex
% ============================================================================
% ScientificDeck Default Preamble (Cunningham/Spina Style)
%   Clean, academic, minimal (Metropolis-inspired without requiring the package)
% ============================================================================
\documentclass[aspectratio=169, 11pt]{beamer}

% =============================================================================
% THEME: Minimal and Clean
% =============================================================================
\usetheme{default}
\usecolortheme{default}

% ---------- colour palette (4 colours) ---------------------------------------
\definecolor{darkblue}{RGB}{0,51,102}
\definecolor{lightgray}{RGB}{245,245,245}
\definecolor{medgray}{RGB}{100,100,100}
\definecolor{accentorange}{RGB}{230,126,34}

% Legacy aliases (so TikZ code compiles without mass-renaming)
\colorlet{navy}{darkblue}
\colorlet{deepnavy}{darkblue}
\colorlet{gold}{accentorange}
\colorlet{warmgold}{accentorange}
\colorlet{coral}{red!70}
\colorlet{sage}{green!60!black}
\colorlet{slate}{medgray}
\colorlet{iceblue}{darkblue!30}
\colorlet{lightice}{lightgray}
\colorlet{offwhite}{white}
\colorlet{midgray}{medgray}
\colorlet{codebg}{lightgray}
\colorlet{codetext}{black}

% ---------- beamer theme settings --------------------------------------------
\setbeamercolor{frametitle}{fg=darkblue, bg=white}
\setbeamercolor{title}{fg=darkblue}
\setbeamercolor{subtitle}{fg=medgray}
\setbeamercolor{structure}{fg=darkblue}
\setbeamercolor{normal text}{fg=black, bg=white}
\setbeamercolor{item}{fg=darkblue}
\setbeamercolor{block title}{fg=white, bg=darkblue}
\setbeamercolor{block body}{fg=black, bg=lightgray}
\setbeamercolor{alerted text}{fg=accentorange}
\setbeamercolor{section in toc}{fg=darkblue}
\setbeamercolor{section number projected}{bg=darkblue, fg=white}
\setbeamertemplate{section in toc}[sections numbered]
\setbeamertemplate{navigation symbols}{}

% ---------- fonts ------------------------------------------------------------
\usefonttheme{professionalfonts}
\setbeamerfont{title}{size=\LARGE, series=\bfseries}
\setbeamerfont{frametitle}{size=\large, series=\bfseries}

% ---------- packages ---------------------------------------------------------
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{microtype}
\usepackage{tikz}
\usetikzlibrary{calc, positioning, arrows.meta, shapes.geometric, shapes.symbols, fit, backgrounds}
\usepackage{tcolorbox}
\tcbuselibrary{skins, breakable}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{xurl}
\usepackage{hyperref}
\usepackage{adjustbox}
\usepackage{etoolbox}
\usepackage{ragged2e}
\usepackage{listings}
\usepackage{amsmath,amssymb}
\usepackage{soul}

% ---------- Global TikZ styles -----------------------------------------------
\tikzset{
  auditbase/.style={draw=none, rounded corners=4pt,
    text width=2.6cm, minimum height=3.3cm, inner sep=6pt, align=center},
  auditlabel/.style={font=\footnotesize\bfseries, text=white},
  audittext/.style={font=\scriptsize, text width=2.3cm, align=left},
  agentbase/.style={draw=none, rounded corners=4pt,
    text width=3.5cm, minimum height=3.0cm, inner sep=6pt, align=center},
  agentlabel/.style={font=\footnotesize\bfseries, text=white},
  agenttext/.style={font=\scriptsize, text width=3.0cm, align=left},
  phasebase/.style={draw=none, rounded corners=4pt,
    text width=2.6cm, minimum height=2.8cm, inner sep=6pt, align=center},
  phaselabel/.style={font=\footnotesize\bfseries, text=white},
  phasetext/.style={font=\scriptsize, text width=2.3cm, align=left},
}

% ---------- safer defaults for graphics --------------------------------------
\setkeys{Gin}{width=\linewidth,height=0.75\textheight,keepaspectratio}

% ---------- Frame title: dark blue text + thin rule --------------------------
\setbeamertemplate{frametitle}{%
  \vspace{0.35cm}%
  \insertframetitle%
  \vspace{0.15cm}%
  \hrule height 0.5pt%
  \vspace{0.25cm}%
}

% ---------- Footer: right-aligned page numbers only --------------------------
\setbeamertemplate{footline}{%
  \hfill\scriptsize\insertframenumber/\inserttotalframenumber\hspace{0.5cm}\vspace{0.3cm}%
}

% ---------- Section break slides ---------------------------------------------
\AtBeginSection[]{%
  \begin{frame}[plain]
  \vfill
  \begin{center}
    {\Large\bfseries\textcolor{darkblue}{\insertsectionnumber}}\\[0.3cm]
    {\LARGE\bfseries\textcolor{darkblue}{\insertsection}}
  \end{center}
  \vfill
  \end{frame}
}

% Make frames forgiving re line breaks
\AtBeginEnvironment{frame}{%
  \setlength{\emergencystretch}{2em}%
}

% ---------- Code listing style -----------------------------------------------
\lstset{
  basicstyle=\ttfamily\scriptsize,
  backgroundcolor=\color{lightgray},
  frame=single, framerule=0pt,
  breaklines=true
}

% ---------- tcolorbox styles (clean, academic) -------------------------------
\newtcolorbox{keyinsight}[1][]{%
  enhanced,
  colback=lightgray, colframe=lightgray, boxrule=0pt,
  borderline north={1.5pt}{0pt}{darkblue},
  sharp corners, left=8pt, right=8pt, top=6pt, bottom=6pt,
  fonttitle=\bfseries\color{white},
  coltitle=white, colbacktitle=darkblue,
  title={#1}
}
\newtcolorbox{quotebox}{%
  enhanced,
  colback=lightgray, colframe=lightgray, boxrule=0pt,
  sharp corners, left=8pt, right=8pt, top=6pt, bottom=6pt,
}
\newtcolorbox{warningbox}[1][]{%
  enhanced,
  colback=lightgray, colframe=lightgray, boxrule=0pt,
  borderline north={1.5pt}{0pt}{darkblue},
  sharp corners, left=8pt, right=8pt, top=6pt, bottom=6pt,
  fonttitle=\bfseries\color{white},
  coltitle=white, colbacktitle=darkblue,
  title={#1}
}
\newtcolorbox{codeblock}{%
  enhanced,
  colback=lightgray, colframe=lightgray, sharp corners,
  left=8pt, right=8pt, top=6pt, bottom=6pt, boxrule=0pt,
  width=\linewidth
}

% ---------- custom commands --------------------------------------------------
\newcommand{\emphgold}[1]{\alert{\textbf{#1}}}
\newcommand{\emphcoral}[1]{\textcolor{red}{\textbf{#1}}}
\newcommand{\emphsage}[1]{\textcolor{green!60!black}{\textbf{#1}}}
\newcommand{\emphslate}[1]{\textcolor{medgray}{#1}}
\newcommand{\cmark}{\textcolor{accentorange}{\texttt{>}}\;\,}
\newcommand{\codett}[1]{{\ttfamily\scriptsize\raggedright\hyphenpenalty=50\exhyphenpenalty=50 #1}}
\newcommand{\sourceref}[1]{\vspace{0.15cm}\hfill{\tiny\textcolor{medgray}{#1}}}
```

## Custom Environments Reference

| Environment | Usage | Visual |
|-------------|-------|--------|
| `keyinsight[Title]` | Key findings, important takeaways | Navy title bar + lightgray body + dark blue top border |
| `quotebox` | Attributed quotes, callouts | Lightgray box, no title |
| `warningbox[Title]` | Warnings, caveats | Same as keyinsight (navy title) |
| `codeblock` | Code snippets in a box | Lightgray, sharp corners |

## Custom Commands Reference

| Command | Output | Use |
|---------|--------|-----|
| `\emphgold{text}` | **Bold orange** | Primary emphasis |
| `\emphcoral{text}` | **Bold red** | Warnings, negative |
| `\emphsage{text}` | **Bold green** | Positive, success |
| `\emphslate{text}` | Gray text | De-emphasized |
| `\cmark` | Orange `>` marker | Bullet alternative |
| `\codett{text}` | Monospace small | Inline code |
| `\sourceref{text}` | Tiny gray right-aligned | Source attribution |

## Section Breaks

Sections auto-generate a plain slide with centered section number + title in dark blue. Use `\section{Title}` and the break appears automatically via `\AtBeginSection`.

## Style Summary

| Aspect | Choice |
|--------|--------|
| Theme | Custom minimal (`\usetheme{default}`, fully overridden) |
| Colors | 4-core: Navy (#003366), Lightgray (#F5F5F5), Medgray (#646464), Orange (#E67E22) |
| Typography | Latin Modern + T1 + microtype + professionalfonts |
| Layout | 16:9 widescreen, 11pt |
| Boxes | tcolorbox (enhanced, sharp corners, navy/gray) |
| Navigation | Disabled, right-aligned frame counter only |
| Frame titles | Bold dark blue + 0.5pt separator rule |
| Section breaks | Auto-generated plain slides (number + title) |
| TikZ | Pre-configured styles for audit/agent/phase diagrams |
| Code | lstlisting with scriptsize mono on lightgray |
| Graphics | Default width=linewidth, height=0.75textheight, keepaspectratio |

## Code-First Figure Workflow

**CRITICAL:** Generate figures BEFORE inserting into LaTeX.

```
1. Write R/Python script → save as code/figures/fig_name.R
2. Run script → output to output/figures/fig_name.pdf
3. Insert into Beamer: \includegraphics[width=\textwidth]{output/figures/fig_name.pdf}
4. Only then compile deck
```

### R Figure Template
```r
library(ggplot2)
p <- ggplot(data, aes(x = var1, y = var2)) +
  geom_point() +
  theme_minimal(base_size = 14) +
  labs(title = NULL, x = "X Label", y = "Y Label")
ggsave("output/figures/fig_name.pdf", p, width = 8, height = 5)
```

### Python Figure Template
```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y)
ax.set_xlabel("X Label")
ax.set_ylabel("Y Label")
fig.savefig("output/figures/fig_name.pdf", bbox_inches="tight")
```

## Two-Column Layout
```latex
\begin{frame}{Claim Supported by Figure}
  \begin{columns}
    \column{0.5\textwidth}
    \begin{itemize}
      \item Key point one
      \item Key point two
    \end{itemize}
    \column{0.5\textwidth}
    \includegraphics[width=\textwidth]{output/figures/fig.pdf}
  \end{columns}
\end{frame}
```

## Table Pattern
```latex
\begin{frame}{Regression Results Show Positive Effect}
  \centering
  \small
  \begin{tabular}{lcc}
    \toprule
    & (1) OLS & (2) IV \\
    \midrule
    Treatment & 0.45*** & 0.62*** \\
              & (0.12) & (0.18) \\
    Controls  & Yes & Yes \\
    N         & 12,000 & 12,000 \\
    \bottomrule
  \end{tabular}
\end{frame}
```
