# Mastering OpenAI Sora: Evidence-Based Prompting Best Practices

OpenAI's Sora video generation model responds best to **detailed, cinematic prompts** that leverage its understanding of physical reality. The model was trained on highly descriptive captions and uses a Diffusion Transformer architecture operating on spacetime patches—meaning it "sees" videos as sequences of related visual concepts across both space and time. This fundamental architecture makes Sora uniquely responsive to structured, film-industry terminology and physics-based descriptions, setting it apart from earlier video generation models.

The most critical insight from OpenAI's own guidance: **"concise, specific directions lead to the most reliable results."** However, "concise" doesn't mean short—it means precisely targeted detail without redundancy. Official example prompts average 60-100 words and include layered descriptions of subject, setting, camera work, lighting, and motion. Sora 2 (released September 2025) adds synchronized audio generation, enabling prompts that specify dialogue, sound effects, and ambient audio alongside visuals.

## Official OpenAI prompt structure framework

OpenAI's help documentation establishes five core components that should appear in effective Sora prompts, derived from analysis of the model's training methodology. These aren't optional flourishes—they align with how Sora's spacetime patch architecture processes visual information.

**Subject and setting** form the foundation: describe who or what appears, where they are, time of day, and atmospheric conditions. The training data captioner was specifically designed to extract these elements, meaning Sora expects them. Example: "A stylish woman walks down a Tokyo street filled with warm glowing neon and animated city signage. The street is damp and reflective, creating a mirror effect of the colorful lights."

**Camera and motion** specifications leverage Sora's emergent 3D consistency capabilities. The model automatically learned to create different camera angles from 2D training data alone, according to researcher Bill Peebles. Use professional terminology: "wide establishing shot," "slow dolly left," "tracking shot following subject," "handheld with slight jitter," "crane shot descending." These terms aren't arbitrary—they map to learned visual patterns in the training data.

**Visual style and pacing** guide the diffusion process across all ~250 denoising steps. Specify film stock ("shot on 35mm film," "70mm cinematic"), color grading ("vivid colors," "muted tones," "desaturated"), lighting quality ("golden hour," "soft diffused light," "dramatic side lighting"), and technical elements like "depth of field" or "bokeh." The model was trained with DALL-E 3's recaptioning technique, which emphasizes visual style descriptions.

**Temporal elements** remain challenging but critical. Lead researcher Tim Brooks acknowledged Sora "has trouble" with "specific camera trajectory over time," but explicit timing helps: "Three-beat gag: wide → medium → close-up; quick cuts" or "The camera starts with a close-up, then slowly pulls back over 5 seconds to reveal the full scene."

**Audio specifications** (Sora 2 only) enable synchronized soundscapes. Describe dialogue, ambient sounds, and audio character: "two friends chatting in a café; clinking cups, soft jazz in background" or "ambient sounds of chiseling, distant birdsong." For multi-speaker scenes, OpenAI recommends keeping casts small and timing clear.

## What makes Sora different: architecture-informed prompting strategies

Sora's Diffusion Transformer architecture—fundamentally different from the U-Net models powering Stable Diffusion or earlier video generators—creates unique prompting opportunities. Understanding these technical foundations explains why certain prompt strategies work.

The **spacetime patch representation** processes video as sequences of visual concepts spanning both spatial dimensions and time. Unlike frame-by-frame approaches, Sora sees relationships between patches across the entire video simultaneously through transformer attention mechanisms. This means prompts should describe relationships: "A woman walks in the foreground with a neon-lit Tokyo street stretching behind her, with pedestrians visible in the background." The spatial hierarchy (foreground/background) and relationships (woman, street, pedestrians) guide the attention mechanism.

**Emergent physics simulation** arose from massive-scale training (estimated 1.1×10²⁵ to 2.7×10²⁵ FLOPS) without explicit physics programming. Tim Brooks noted "the model figured out how to create 3D graphics from its dataset alone." This creates a crucial prompting principle: **physically plausible descriptions produce more consistent results**. Specify material properties ("rough wood," "flowing silk fabric," "water splashing"), forces ("wind gently blowing," "heavy rain falling"), and realistic physics. Sora 2 significantly improved here—a basketball now bounces off the backboard rather than teleporting to the hoop.

The **latent diffusion mechanism** iteratively denoises over multiple steps, with your prompt guiding each step. Comprehensive prompts provide consistent direction throughout generation, while vague prompts leave more steps to chance. This differs from single-pass models where prompt detail matters less.

**Native resolution training** on videos from widescreen 1920×1080p to vertical 1080×1920p means Sora composes shots naturally for specified formats. Earlier models cropped everything to squares, creating awkward framing. Specify format when relevant: "cinematic widescreen 16:9" for landscape content, "vertical 9:16 mobile format" for social media, "square 1:1" for Instagram.

## Concrete examples from OpenAI: analyzing what works

OpenAI's original announcement included meticulously crafted example prompts that reveal the company's internal best practices. These aren't casual demonstrations—they represent ideal prompt structure.

**Example 1: The Tokyo street woman** (79 words) demonstrates layered detail without redundancy. Subject details establish character: "black leather jacket, long red dress, black boots, black purse, sunglasses, red lipstick." Action is simple but specific: "walks confidently and casually." Environment gets atmospheric treatment: "warm glowing neon," "damp and reflective street," "mirror effect of colorful lights." The prompt includes contextual elements: "many pedestrians walk about." Every descriptor serves a purpose—no filler words.

**Example 2: Woolly mammoths** (76 words) showcases physics and cinematography. Material properties: "long woolly fur lightly blows in the wind." Environmental depth: "snow covered trees and dramatic snow capped mountains in the distance." Lighting specificity: "mid afternoon light with wispy clouds and a sun high in the distance creates a warm glow." Camera work: "low camera view is stunning capturing the large furry mammal with beautiful photography, depth of field." This prompt treats Sora like a cinematographer who understands composition.

**Example 3: Sora 2 advanced format specification** represents evolved prompting techniques. The prompt explicitly separates concerns: "Primary Target & Visuals: First read: a dragon slicing past serrated ice spires, wingtip vortices peeling spindrift; second read: the glacier's fractured sheet falling away to a cobalt fjord... Format & Look: 5.0s; 4K; 180° shutter; large-format digital sensor emulation with crisp micro-contrast; very fine grain." This structure—conceptual description followed by technical specifications—mirrors professional cinematography briefs.

**Example 4: Extreme close-up** (28 words) proves brevity works when precision is high: "Extreme close up of a 24 year old woman's eye blinking, standing in Marrakech during magic hour, cinematic film shot in 70mm, depth of field, vivid colors, cinematic." Every word carries specific meaning: "extreme close up" (shot type), "eye blinking" (action), "magic hour" (lighting), "70mm" (format), "depth of field" (focus technique), "vivid colors" (grading).

The pattern across all official examples: **No wasted words, maximum information density, professional terminology, layered detail.**

## Technical terminology that works: camera, lighting, physics

Sora's training data captioner was designed to extract technical terminology from professional video descriptions. The model recognizes and responds to industry-standard terms that might seem jargon-heavy.

**Camera shot types** establish framing and composition. Use: "extreme close-up" (ECU), "close-up," "medium shot," "wide shot," "extreme wide shot" (EWS), "establishing shot," "over-the-shoulder," "point-of-view" (POV), "bird's-eye view," "low angle," "high angle," "Dutch angle" (tilted). These terms carry specific compositional implications the model understands.

**Camera movements** guide temporal flow. Effective terms include: "tracking shot" (following subject), "dolly in/out" (camera moves toward/away), "crane shot" (vertical movement), "pan left/right" (horizontal camera rotation), "tilt up/down" (vertical rotation), "handheld" (shakier, documentary feel), "steadicam" (smooth movement), "drone view" (aerial perspective), "static shot" (no movement). Tim Brooks noted complex camera trajectories remain challenging, but named movements work better than vague descriptions.

**Lighting terminology** dramatically affects mood and visual quality. Use: "golden hour" (warm sunset light), "magic hour" (twilight), "blue hour" (deep twilight), "harsh midday sun," "overcast," "soft diffused light," "dramatic side lighting," "rim lighting," "backlighting," "three-point lighting," "practical lights" (visible light sources in frame), "volumetric lighting" (light beams through atmosphere), "ambient lighting."

**Film format specifications** inform the look. Reference: "shot on 35mm film," "70mm cinematic," "Super 8mm," "16mm," "iPhone-style realism," "IMAX," "anamorphic lens," "large-format digital sensor." Include technical details: "shallow depth of field," "deep focus," "bokeh," "lens flare," "film grain," "180° shutter," "high shutter speed," "motion blur."

**Physics and material properties** leverage Sora's emergent simulation capabilities. Describe: fabric movement ("silk flowing in breeze," "heavy coat barely moving"), liquid behavior ("water splashing," "slow-motion droplets"), particle effects ("dust particles floating in light beam," "snow drifting"), surface properties ("reflective wet pavement," "rough stone texture," "smooth polished metal"), and forces ("gentle breeze," "strong gusting wind," "objects falling with weight").

## Known limitations and workarounds from the research team

Tim Brooks and the Sora team have been remarkably transparent about current weaknesses, providing crucial guidance on what to avoid or how to structure prompts around limitations.

**Hands and walking remain problematic.** Brooks stated directly: "Hands in general are a pain point." Community testing revealed "legs cross over and merge into each other" during walking sequences. **Workaround**: Use wider shots where hands and feet are less prominent, specify "hands at sides" or "hands in pockets" for clearer constraints, or avoid close-ups of complex hand movements. For walking, specify "confident stride" or "casual walk" rather than detailed gait descriptions.

**Complex physics interactions fail.** Brooks acknowledged "some aspects of physics" cause problems. OpenAI's technical report gives an example: eating a cookie might not show a bite mark. Multiple object collisions become unpredictable. **Workaround**: OpenAI recommends "simpler motion," "fewer characters," and breaking complex interactions into separate generations. Instead of "person catches falling vase," try "person reaching toward falling vase" and generate the catch separately.

**Specific camera trajectories over time struggle.** Brooks noted, "If you ask for really specific, like camera trajectory over time, it has trouble doing that." **Workaround**: Use named camera movements ("tracking shot," "dolly zoom") rather than precise path descriptions. Instead of "camera moves in arc from left to right, then up 45 degrees," use "circling crane shot" or break into multiple shots.

**Spatial relationships occasionally confuse.** The technical report acknowledges Sora may "confuse spatial details included in a prompt, such as discerning left from right." **Workaround**: Use relative positioning ("in the foreground," "behind the subject," "to the left of the tree") with clear reference points rather than absolute directions. Verify critical spatial relationships in iterations.

**Cause and effect relationships may break.** The model doesn't always maintain logical consequences of actions. **Workaround**: Simplify action sequences, explicitly state consequences in the prompt ("basketball bounces off backboard and falls to ground"), or generate complex sequences as multiple separate videos.

**Multi-character scenes with dialogue prove difficult.** OpenAI specifically notes Sora 2 "can struggle with scenes containing many people speaking at once." **Workaround**: "Keep casts small and timing clear." For dialogue scenes, specify "two friends chatting, one at a time" and describe turn-taking explicitly.

## Optimal prompt length and structure

No official character limit exists in OpenAI documentation, but analysis of example prompts and researcher commentary reveals practical patterns.

**Optimal length: 50-120 words** for most prompts. OpenAI's own examples cluster in this range. Shorter prompts (20-40 words) work when ultra-specific: "Extreme close up of a 24 year old woman's eye blinking, standing in Marrakech during magic hour, cinematic film shot in 70mm, depth of field, vivid colors." Longer prompts (120-200 words) can work for complex scenes but risk diluting focus—OpenAI recommends "shorter prompts" as a troubleshooting step.

**Information density matters more than length.** The recaptioning technique means Sora was trained on highly descriptive but efficient captions. Avoid redundancy: don't say "beautiful, stunning, gorgeous lighting"—choose one descriptor. Instead of "walking slowly and gradually," use "ambling" or "strolling."

**Structure prompts hierarchically** from most to least important. Start with core subject and action, add setting and atmosphere, then layer technical specifications. This mirrors how the diffusion process works—early denoising steps establish overall composition, later steps refine details.

**The "and" test** reveals bloat. If you're stringing together many "and" clauses, you're likely over-specifying. "A woman walking down a street and wearing sunglasses and carrying a purse and wearing boots" is worse than "A woman in sunglasses walks down a street, carrying a black purse, wearing black boots." Use commas and subordinate clauses for better flow.

**Iterate by addition, not replacement.** OpenAI's help center recommends: "Start with the core intent; add camera, motion, and pacing on the next pass." Generate with a basic prompt, identify what needs specification, then add targeted detail. Don't rewrite the entire prompt each iteration.

## Temporal elements and motion specification techniques

Temporal consistency—Sora's ability to maintain coherent scenes over time—is both a strength and a challenge requiring careful prompt engineering.

**Specify duration implicitly through action complexity.** While you can't directly control video length in basic prompts (Sora 2 defaults to 10 seconds), action complexity influences pacing. "A woman walks down a street" suggests continuous motion filling the duration. "A woman walks down a street, stops to look in a shop window, then continues walking" suggests a three-part temporal structure Sora will attempt to fit into the timeframe.

**Use temporal markers** for multi-part sequences. "First, the camera shows... then... finally" creates clear progression. "Three-beat gag: wide → medium → close-up; quick cuts" explicitly structures timing. Be specific about sequence: "The camera starts with a close-up of the woman's face, then slowly pulls back over 5 seconds to reveal the full street scene."

**Motion descriptors** should match desired pacing. **Slow motion**: "slow motion," "languid," "drifting," "floating," "deliberate." **Normal speed**: "walking," "running," "moving." **Fast motion**: "darting," "rapid," "quick cuts," "frenetic," "time-lapse." **Static shots**: "still shot," "subject remains motionless," "camera fixed on."

**Camera motion affects perceived time.** "Slow dolly left" feels contemplative. "Rapid pan across scene" feels energetic. "Static shot" emphasizes subject movement. Match camera motion to desired mood and pacing.

**The storyboard feature** (Sora 2) enables precise temporal control. Create cards for specific timestamps, describing or uploading images for key moments. OpenAI recommends: "Leave space between cards to give time to connect scenes. The less space between cards, the higher likelihood of hard cuts." This is the most precise temporal control method available.

**Object permanence and continuity** generally work well—Sora's transformer architecture maintains character and visual style across shots. Researchers demonstrated this with examples like "a walking figure made out of water tours an art gallery"—the paintings remain consistent throughout. Leverage this by confidently describing persistent elements: "The woman's red dress remains vivid as she moves through different lighting conditions."

## Character and scene description best practices

Creating believable, consistent characters and environments requires strategic detail distribution based on what Sora's architecture prioritizes.

**Character appearance**: Specify 3-5 distinctive features rather than exhaustive descriptions. "Black leather jacket, long red dress, black boots, sunglasses, red lipstick" (from OpenAI example) gives enough to establish identity without overwhelming. Include: primary clothing, distinctive accessories, one or two facial features, general demeanor ("confident," "cautious," "energetic").

**Character emotions and demeanor** work better than facial expressions. Instead of "smiling widely with eyebrows raised," use "expressing joy" or "looking surprised." The model understands emotional states: "deep in thought," "pondering," "expressing predatory calm/effortless power" (from OpenAI's dragon example). Brooks confirmed "the model can generate compelling characters that express vibrant emotions."

**Multiple characters require careful limitation.** OpenAI explicitly recommends "fewer characters" as a workaround for quality issues. For multi-character scenes: clearly distinguish characters ("one in red, one in blue"), specify their spatial relationship ("standing side by side," "facing each other"), describe their interaction ("chatting," "arguing," "dancing together"). Avoid crowds with specific individuals—use "many pedestrians walk about" for background elements.

**Scene environments** benefit from layered depth. OpenAI's mammoth prompt demonstrates this: "snowy meadow" (ground), "snow covered trees" (mid-ground), "dramatic snow capped mountains in the distance" (background). Establish foreground, middle, and background explicitly to leverage Sora's 3D consistency.

**Atmospheric elements** create immersion. Weather: "heavy rain," "light drizzle," "snow falling gently," "overcast sky." Time: "dawn breaking," "midday sun," "dusk," "night with streetlights." Particles: "dust in air," "mist," "smoke," "light streaming through windows." These elements fill the scene with dynamic detail.

**Environmental interaction** grounds characters in the world. "The street is damp and reflective, creating a mirror effect" (OpenAI example) shows active use of environmental properties. "Footsteps leaving prints in snow," "hair blowing in wind," "rain dripping off clothing"—these details leverage Sora's physics simulation.

**Branded items won't work.** Brooks noted in interviews that "branded items never quite match up to real life." Don't prompt for "iPhone 15" or "Tesla Model 3"—use generic descriptions: "smartphone," "sleek electric car." This is partly intentional to avoid IP issues.

## Audio and sound design specifications for Sora 2

Sora 2's synchronized audio generation opens new prompting dimensions, but requires understanding how the audio model works alongside video generation.

**Audio is generated simultaneously with video**, not added post-production. The prompt guides both modalities together, meaning audio descriptions should integrate with visual descriptions rather than appearing as afterthoughts.

**Dialogue specification** requires character identification and turn-taking. "Two friends chatting in a café" generates ambient conversation. For specific content: "Two mountain explorers in bright technical shells, ice crusted faces, eyes narrowed with urgency shout in the snow, one at a time." The "one at a time" is critical—simultaneous speech confuses the model.

**Ambient sound and atmosphere** fill the sonic environment. Describe: room acoustics ("echoing warehouse," "intimate acoustic space"), background activities ("clinking cups, soft jazz" for café, "distant traffic, birds chirping" for outdoor), weather sounds ("rain pattering on roof," "wind howling"), and mechanical sounds ("machinery humming," "computer fans").

**Sound effects** (foley) should match actions. If someone walks, you'll get footsteps automatically, but you can specify: "footsteps echoing on marble floor," "soft footfalls on carpet," "boots crunching in snow." Match materials: "glass breaking," "wood creaking," "metal clanging."

**Music and score** can be suggested but shouldn't be too specific about copyrighted works. Use genre and mood: "upbeat electronic music," "melancholic piano," "dramatic orchestral score," "lo-fi beats," "ambient synth pads." Or reference styles: "90s hip-hop beat," "baroque chamber music," "synthwave."

**Audio perspective** should match camera position. A close-up naturally brings dialogue forward; a wide shot makes it more ambient. You can specify: "close-mic dialogue" for intimacy, "distant conversation" for atmosphere, "POV audio" for immersive first-person.

**Avoid audio when inappropriate.** Not every scene needs dialogue or music. "Ambient sounds only" or "natural environmental audio" keeps things realistic. Silence isn't an option with Sora 2—it generates audio automatically if it "makes sense for the scene."

**Known limitation**: "Scenes containing many people speaking at once" struggle. The model can't reliably separate multiple simultaneous speakers. Design scenes with clear audio focus.

## Iterative refinement workflow

Sora isn't a one-prompt-perfect-output system. The researchers emphasize feedback-driven iteration, and OpenAI's help documentation explicitly recommends "Remix" features for branching variations.

**Start broad, refine narrow.** Begin with core subject and action in 20-30 words. Generate and assess whether the concept works. If yes, add camera specifications in the next iteration. Then add lighting and atmosphere. Finally, add technical specifications. This progressive refinement aligns with how the diffusion process works—early decisions establish composition, later decisions add detail.

**Identify specific problems** rather than saying "make it better." Did hands merge? Add "hands at sides." Is motion too fast? Add "slow, deliberate movement." Is lighting wrong? Specify "golden hour lighting" or "overcast daylight." Targeted fixes work better than wholesale prompt rewrites.

**Use the Remix feature** (Sora 2) to branch variations without losing good results. OpenAI recommends: "Keep versions clean—Remix instead of overwriting good takes." Generate multiple variations with slight prompt adjustments, then compare outputs.

**Test single-variable changes** when troubleshooting. Change one element (camera angle, lighting, action complexity) and regenerate. This isolates what affects output. If you change five things simultaneously, you can't identify what caused improvements or degradations.

**Build a prompt library** of effective phrasings. When you find descriptions that work consistently ("damp reflective street creating mirror effect," "golden hour creating warm glow," "low camera view capturing subject with beautiful photography"), save them for reuse in similar contexts.

**Physics debugging**: If physics look wrong, simplify interactions first. Remove complex collisions, reduce moving objects, make motion more straightforward. Only add complexity back when basic physics work correctly.

**Temporal debugging**: If temporal flow breaks, add explicit sequence markers. "First... then... finally." Specify duration hints through pacing terms: "slow," "quick," "gradual."

## What to avoid: anti-patterns from research

Analysis of limitations and failed examples reveals clear anti-patterns that waste iterations.

**Don't over-specify impossible physics.** Prompts like "water flowing upward in a spiral while also splashing downward" fight Sora's physics simulation. Creative physics work (walking water figure), but contradictory physics confuse the model. Unless you explicitly want surrealism, respect basic physical laws.

**Avoid ambiguous spatial relationships.** "The cup is near the edge but also in the center" creates confusion. Use clear, consistent spatial language. Pick a spatial reference frame and stick to it.

**Don't prompt for specific camera trajectories as mathematical paths.** "Camera moves in arc from coordinates (0,0) to (5,3) to (2,7)" means nothing to Sora. Use cinematic language: "sweeping crane shot," "orbiting the subject," "descending from above."

**Don't expect specific branded products.** "iPhone 15 Pro Max," "Nike Air Jordans," "Coca-Cola can" won't render accurately. Generic equivalents appear instead. Use generic descriptions for believable results.

**Avoid complex multi-character choreography.** "Three people simultaneously jump, high-five, and spin" exceeds current capabilities. Brooks confirmed complex interactions struggle. Simplify to pairs or focus on one primary character with others as background.

**Don't use vague aesthetic terms alone.** "Make it beautiful" or "cinematic" without specifics leaves too much to chance. "Beautiful" how? "Cinematic" like what? Add concrete visual elements: "beautiful golden-hour lighting illuminating the scene" or "cinematic 70mm anamorphic lens with shallow depth of field."

**Don't neglect setting and atmosphere.** Prompts like "A woman walks" generate something, but without environmental detail, Sora fills in randomly. "A woman walks down a Tokyo street filled with neon signage" gives the model clear context.

**Avoid writing in multiple conflicting styles.** "Hyperrealistic photographic shot in anime style with claymation textures" confuses aesthetic coherence. Pick one primary style and stick to it, perhaps with one complementary element.

## Comparison to other video models

Understanding Sora's unique capabilities helps you leverage features other models lack.

**Duration**: Sora generates up to 60 seconds (original), while Pika and Runway Gen-2 typically max at 4 seconds. This enables complex narratives and full scene development. Prompt accordingly—Sora can handle multi-part sequences that would require stitching in other tools.

**3D consistency**: Academic research (Li et al., 2024) demonstrated Sora videos enable successful 3D reconstruction, while Pika and Gen-2 videos cannot. This means Sora maintains geometric coherence through camera movement. **Prompting advantage**: Confidently specify complex camera movements knowing spatial relationships will hold.

**Physics simulation**: Sora 2 models realistic physics (basketball bouncing off backboard), while earlier models often "cheat" by morphing reality to fulfill prompts (ball teleporting to hoop). **Prompting advantage**: Describe realistic physical interactions and trust they'll render plausibly.

**Multi-shot generation**: Sora can generate multiple shots within a single video maintaining character and style consistency. Other models generate single continuous shots. **Prompting advantage**: Describe shot sequences: "Wide establishing shot, then cut to medium shot, then close-up."

**Resolution and aspect ratio flexibility**: Sora trains on native resolutions from widescreen to vertical, generating clean compositions for any format. Other models often crop, creating awkward framing. **Prompting advantage**: Specify format and composition appropriate for that format.

**Instruction following**: The DALL-E 3 recaptioning technique makes Sora better at following complex, detailed instructions than earlier models. **Prompting advantage**: More detail generally helps rather than confuses—opposite of some earlier models where simple prompts worked better.

## Safety constraints and content policies

Understanding what Sora won't generate saves iteration time and prevents policy violations.

**Blocked content categories** (from System Card): extreme violence, sexual content, hateful imagery, child sexual abuse materials, sexual deepfakes, celebrity likeness (text-to-video), others' intellectual property, and generating videos of real people without consent (except Cameos feature).

**Text classifier** filters prompts before generation. Certain words or combinations trigger automatic rejection. Frame creative concepts carefully—violence in context of action movies might work while gratuitous violence won't.

**Celebrity and public figure restrictions**: You cannot generate videos of named real people via text prompts. "Taylor Swift walking down the street" will be blocked. Generic descriptions work: "a pop star walking down the street." The Cameos feature allows generating videos of yourself with explicit consent.

**Intellectual property constraints**: Prompts referencing specific copyrighted characters, brands, or properties may be blocked or produce generic equivalents. "Spider-Man swinging through New York" likely fails; "A superhero in a red and blue costume swinging through a city" works.

**Misinformation concerns**: While not explicitly filtered in prompts, OpenAI emphasizes responsible use. Avoid prompting for realistic footage of events that didn't happen, particularly involving public figures or institutions, as this enables misinformation.

**Detection and watermarking**: Generated videos can be identified by OpenAI's detection classifier. C2PA metadata is planned for tracking content provenance. Assume Sora-generated content can be identified as AI-generated.

## Advanced techniques: storyboarding and multi-modal prompting

Beyond text prompts, Sora 2 offers advanced control mechanisms that enable more precise creative direction.

**Storyboard feature** enables frame-by-frame control. Create cards for specific timestamps, each containing text descriptions, uploaded images, or video clips. The model generates transitions between cards. **Best practice**: "Leave space between cards to give time to connect scenes. The less space between cards, the higher likelihood of hard cuts." This enables precise narrative control impossible with single text prompts.

**Image-to-video** (animating still images) lets you provide visual reference and describe desired motion. Effective for: animating DALL-E 3 generated images, bringing photos to life, or starting from specific visual composition. Prompt focuses on describing the animation: "Camera slowly zooms in while subject turns head to look at camera."

**Video-to-video editing** transforms existing footage. Change style ("transform to anime style"), alter setting ("change summer scene to winter"), or modify atmosphere ("make scene stormy and dramatic"). The model maintains core composition while applying transformations. Useful for rapid style exploration.

**Video extension** adds footage before or after existing clips. Describe what should happen: "Continue this scene with the subject walking away from camera" or "Show what happened before this moment." Maintains visual consistency with the original.

**Video blending** creates seamless morphs between completely different scenes. Bill Peebles highlighted this as "entirely new types of content." Prompt describes the transformation: "Gradually morph from ocean waves to desert dunes, maintaining the rolling motion."

**Combining techniques**: Start with image-to-video to establish composition, extend to add length, remix to explore variations, then use storyboard to assemble final sequence. Multi-modal workflows offer control impossible with text alone.

## The prompt engineering mental model

Synthesizing all research, the most effective mental model treats Sora as a **cinematographer with physics understanding but imperfect execution**. You're providing a creative brief to a skilled but occasionally confused collaborator.

**Speak the language of film production.** Sora was trained on professional video descriptions. Using industry terminology (shot types, camera movements, lighting setups, film formats) aligns with its training data distribution. You're not writing poetic descriptions—you're giving technical direction.

**Describe reality accurately.** Sora learned physics and 3D consistency from observing reality. Prompts describing plausible physics produce coherent results. Fight against physics and consistency breaks down. This doesn't mean you can't be creative—walking water figures work—but internal physics should be coherent.

**Layer information hierarchically.** The diffusion process iteratively refines from noise to image. Early steps establish composition; later steps add detail. Structure prompts similarly: subject and action first (composition), then setting (context), then camera and lighting (refinement), finally technical specifications (polish).

**Guide attention with relationships.** Transformer architectures process information through attention mechanisms. Describing how elements relate (spatially, temporally, causally) helps the attention mechanism understand your intent. "A woman in the foreground with a street behind her" is clearer than "a woman and a street."

**Iterate scientifically.** When results miss the mark, identify the specific divergence and add targeted constraints. Change one variable at a time. Build prompt libraries of effective phrasings. Treat prompting as an experimental process with learnable patterns.

**Respect limitations transparently.** The Sora team has been explicit about current weaknesses. Don't fight against documented limitations—work around them. Simplify complex physics, reduce character count, use named camera movements, break impossible sequences into multiple generations.

**Think in spacetime patches.** Sora doesn't see individual pixels or frames—it processes patches across space and time simultaneously. Describing how visual elements persist and transform through both spatial and temporal dimensions aligns with this architecture.

## Conclusion: from understanding to mastery

Effective Sora prompting emerges from understanding its architectural foundation—Diffusion Transformers operating on spacetime latent patches, trained on highly descriptive captions at massive scale. This isn't arbitrary: the model's strengths (long-form generation, 3D consistency, physics simulation, instruction following) and weaknesses (complex hand movements, specific camera trajectories, multi-character choreography) all stem from this architecture.

The evidence from OpenAI documentation, technical papers, and researcher interviews converges on clear principles: use detailed but efficient descriptions, employ professional cinematography terminology, respect physics, describe relationships explicitly, specify temporal progression, and iterate systematically. Sora responds to prompts that treat it as a skilled cinematographer working from a detailed creative brief.

What distinguishes expert Sora prompting from novice attempts isn't prompt length or fancy language—it's information density, structural clarity, and alignment with how the model processes visual information. Every word in your prompt should guide the spacetime patch attention mechanism toward your creative vision. OpenAI's own example prompts achieve 60-100 words of pure signal with zero noise.

As Sora continues scaling (following predictable AI scaling laws), expect improved physics handling, longer generation capacity, and better complex interaction modeling. Current prompting strategies will only become more powerful. Master the fundamentals now—detailed description, cinematic language, physics awareness, relationship specification—and you're prepared for whatever capabilities emerge next.

The researchers built Sora as a "world simulator" that understands physical reality. Your prompts should describe the world you want simulated with the precision and clarity of a cinematographer's shot list. That's the art and science of Sora prompt engineering.