# HTML Slide Engine

## Base Engine
```css
.deck { height: 100dvh; overflow-y: auto; scroll-snap-type: y mandatory; scroll-behavior: smooth; }
.slide { height: 100dvh; scroll-snap-align: start; overflow: hidden; display: flex; flex-direction: column; justify-content: center; padding: clamp(40px, 6vh, 80px) clamp(40px, 8vw, 120px); }
```

## Typography Pairings
| Pairing | Body | Mono | Best For |
|---------|------|------|----------|
| Academic Classic | Crimson Pro | Noto Sans Mono | Research seminars |
| Technical | IBM Plex Sans | IBM Plex Mono | Technical talks |
| Reading-Optimized | Literata | Source Code Pro | Teaching |
| Modern Academic | Sora | IBM Plex Mono | Conference talks |

## Type Scale
| Element | Size | Weight |
|---------|------|--------|
| Display | clamp(48px, 10vw, 120px) | 800 |
| Heading | clamp(28px, 5vw, 48px) | 700 |
| Body | clamp(16px, 2.2vw, 24px) | 400 |
| Code | clamp(14px, 1.8vw, 18px) | 400 |
| Label | clamp(10px, 1.2vw, 14px) | 600 |

## Color Palettes

### Academic Slate (default)
Light: `--bg: #f8f6f2; --text: #1e3a5f; --accent: #c44536`
Dark: `--bg: #0f1923; --text: #e0ddd5; --accent: #e85d4a`

### Paper & Ink
Light: `--bg: #faf6f0; --text: #2c2c2c; --accent: #8b4513`

### Nordic Science
Light: `--bg: #eceff4; --text: #2e3440; --accent: #5e81ac`

## Navigation
- Progress bar (fixed top, 3px, accent color)
- Slide counter (fixed bottom-right, mono)
- Keyboard: Arrow keys + Space for navigation
- Cinematic transitions via IntersectionObserver (.visible class)
