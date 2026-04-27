# WebGLFrontier Workflow

Level 7 — The Frontier. Custom WebGL, shaders, 3D experiences. Websites that look like video games. This is aspirational — it shows what's possible and provides a starting point when the ambition is there.

## Reality Check

From the source video: "None of us are probably going to be playing at this level" (as of 2026). These sites are typically built by dedicated design teams with custom art and deep WebGL knowledge. What we can do: start small with Three.js basics and build up.

## Inspiration Sources

Before attempting 3D web experiences, study what's possible:

- **Awwwards Sites of the Day/Month** — [awwwards.com](https://awwwards.com) — the gold standard for creative web
- **Three.js Examples** — [threejs.org/examples](https://threejs.org/examples) — official demo gallery
- **Codrops** — [tympanus.net/codrops](https://tympanus.net/codrops) — WebGL tutorials and experiments
- **Bruno Simon's Portfolio** — [bruno-simon.com](https://bruno-simon.com) — the benchmark for 3D web
- **Lusion** — [lusion.co](https://lusion.co) — studio doing cutting-edge WebGL work

## What's Actually Achievable (Solo + Claude Code)

### Tier A: Doable Now

These use Three.js with minimal custom shader knowledge:

**3D Background Scene**
```
Create a Three.js scene with floating geometric shapes (spheres, torus, icosahedrons)
slowly rotating and drifting. Dark background, [ACCENT COLOR] lighting.
Render as a full-screen background behind the page content.
Use OrbitControls with autoRotate but disable user interaction.
```

**Particle Field**
```
Create a Three.js particle system with 5000 points arranged in a [sphere/plane/custom shape].
Particles should gently drift with Perlin noise movement.
Color: monochrome with [ACCENT COLOR] highlights on closest particles.
Mouse interaction: particles near cursor should repel slightly.
```

**3D Text**
```
Create extruded 3D text using Three.js TextGeometry with [FONT].
Apply a metallic material with environment map reflection.
Subtle rotation on mouse move (parallax tilt effect).
```

### Tier B: Stretch Goals

These require some shader knowledge or heavy Three.js work:

- **Custom shaders** — Vertex displacement, post-processing effects (bloom, chromatic aberration)
- **Scroll-bound 3D scenes** — Camera path follows scroll position through a 3D environment
- **GLTF model loading** — Import 3D models and display them interactively
- **Physics simulations** — Cannon.js or Rapier for physical interactions (dragging, throwing, colliding)

### Tier C: Team-Level (Aspirational)

- Full 3D environments with custom lighting
- Real-time fluid simulations
- Procedural generation (terrain, vegetation, cities)
- WebXR/VR experiences

## Getting Started Workflow

1. **Pick a Tier A effect** from above
2. **Use Site Teardown** (Level 4) on an Awwwards site that uses the effect you want
3. **Source the Three.js setup** from the official examples or CodePen
4. **Paste into Claude Code** with adaptation instructions
5. **Iterate** using the Visual Editor Loop (Level 6) for placement and integration

```
I want to add a [TIER A EFFECT] to my website.
Here's a reference implementation from Three.js examples: [PASTE CODE]
Adapt it to:
- Match my color palette: [HEX CODES]
- Render behind my existing page content (z-index layering)
- Be performant on modern devices (target 60fps)
- Gracefully degrade on mobile (reduce particle count, disable on low-end)
- Not block page load (lazy-init the 3D scene after DOM ready)
```

## Performance Rules for 3D Web

These are non-negotiable:

1. **Lazy initialization** — Don't block page load with Three.js setup. Init after `DOMContentLoaded` or on first scroll.
2. **Resize handling** — Listen for `resize` events. Update camera aspect ratio and renderer size.
3. **RequestAnimationFrame** — Never use `setInterval` for render loops.
4. **Dispose on unmount** — Clean up geometries, materials, textures, and renderer when leaving the page.
5. **Mobile detection** — Reduce complexity on mobile: fewer particles, lower resolution, simpler shaders. Or skip 3D entirely and show a static fallback.
6. **GPU budget** — Target 60fps on a mid-range laptop (2020 MacBook Air). If it stutters there, simplify.

## Three.js Starter Template

Minimal setup for adding a 3D background to an existing HTML page:

```html
<canvas id="bg-canvas" style="position:fixed;inset:0;z-index:-1;pointer-events:none;"></canvas>
<script type="module">
  import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170/build/three.module.js';

  const canvas = document.getElementById('bg-canvas');
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 5;

  // Add your objects here

  function animate() {
    requestAnimationFrame(animate);
    // Update animations here
    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
</script>
```

## Relationship to Other Workflows

- **Site Teardown** — Use to reverse-engineer how Awwwards sites implement their 3D effects
- **ComponentSourcing** — CodePen has many Three.js examples to source from
- **GenerateAssets** — AI-generated textures and environment maps for 3D scenes
- **PolishChecklist** — Apply after 3D integration for loading states and performance guards
