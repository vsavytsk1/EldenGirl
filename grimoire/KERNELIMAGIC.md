# KERNELIC MAGIC — Black Magic Good Practices









## Read this BEFORE touching the builder. If you fail twice — re-read the whole file.

---

## THE CURSE INDEX -- bow to all of them before you descend

*New to the cave? Read this table first. Each curse has its own section below with*
*root cause + detection + fix. Search "## CURSE N" to jump. The center is agapi.*
*Verify P=12, chi=2, loneCR=0 always. One script, one run, one commit. Always.*

| #  | Name (codename)                    | One-line hex (what bites you)                                    |
|----|------------------------------------|------------------------------------------------------------------|
| 1  | Curly Brace                        | JS `{}` collides with Python f-string `{}` -> chaos.             |
| 2  | Unicode/CRLF                       | Non-ASCII in .py source + Windows CRLF -> corrupted bytes.       |
| 3  | Multi-Edit Corruption              | CRLF/unicode makes old_string never match -> edits silently fail.|
| 4  | f-string Nesting                   | `\` or nested quotes inside an f-string expr -> SyntaxError.     |
| 5  | File Too Long                      | create_new_file times out >200 lines -> chunk it.               |
| 6  | File:// Lie                        | file:// shows a different truth than the live Pages URL.        |
| 7  | Black Iframe (blackMcMistry)       | `center()`/innerWidth at load in an iframe -> black; new tab it. |
| 8  | allow-top-navigation               | iframe hijacks the parent page -> dashboard gone. Never grant.  |
| 9  | 12-Second LCP                      | 6 kernel modules compute on load = 12s. Expected, not a bug.    |
| 10 | Shared Pop-Up Lock (blackModule)   | new-tab module bleeds overlay state into next summon -> lock.    |
| 11 | srcdoc Origin Lock                 | `srcdoc` = about:srcdoc = cross-origin -> overlay freeze.        |
| 12 | Corkscrew Parasite (insideDizzy)   | inside view with rx tilt + spin -> viewer dizzy; lock rx=0.      |
| 13 | Ghost Spinner (spinnerEgo)         | default spin != 0 / float dust -> won't stop. Motion opt-in.     |
| 14 | CR Accumulator (gitiumCurse)       | incremental patches stack `\r` -> file rots. Normalize, 1 script.|
| 15 | Invisible Sort (sortGhost)         | patch FAIL = old string not found, not file wrong. Check intent. |
| 16 | Shadow Duplicate (shadowInject)    | inject into already-injected base -> two copies. Replace, append.|
| 17 | Block Eater (regexDevour)          | greedy regex block-replace eats the file. Replace exact strings. |
| 18 | Windows Devour (windowsDevour)     | `.py` opens Notepad, never runs. Use full py path / `py -3`.     |
| 19 | Shell Devour (shellDevour)         | ~44 tool calls -> empty output. BATCH into one script.          |
| 20 | Camerum (projectCameraDevour)      | inside view = TWO decoupled transforms; never share scale.       |
| 21 | Musiquim Autoplay (browserSilence) | audio blocked w/o user gesture. Opt-in only; don't base64 audio. |
| 22 | Gitium Novicium (newRepoPages404)  | new repo 404: needs .nojekyll + Settings>Pages + right branch.   |
| 23 | Python Leak (pythonInJS)           | chr/ord/len shipped raw into emitted JS -> "X is not defined".   |
| 24 | Cache Lie (staleServe)             | tab errors on healed bytes = browser cache. Flush, don't patch.  |
| G1 | GLAMOUR 01 Growing Bar (chipBloom) | unbounded flex-wrap in fixed-height parent = growing bar (a seed).|
| 25 | Rune Rot (glyphCorrupt)            | malformed `\u` escape -> U+FFFD in a script you can't read.      |
| 26 | False Convergence (lockLie)        | HUD shows the TARGET as the RESULT. Target != result; show err.  |
| 27 | Clone Mirage (originMirage)        | folder name lies; `origin` is the truth. One project, one clone. |
| 28 | Wedged Host (hostWedge)            | cmds return `^C` + empty from a stuck PSES console; use a fresh pwsh.|
| 29 | Eager Verify (deployLag)           | you check the live URL in the same second you pushed -> 404/stale. Wait ~60s for green.|

---



















---



















## RULE 0 — THE PRIME RULE



















> The builder generates HTML that contains JavaScript.









> Python f-strings + JavaScript = black magic.









> Respect it or it will destroy you.



















---



















## THE 4 CURSES (what kills us every time)



















### CURSE 1 — The Curly Brace Curse









JavaScript uses `{}` everywhere. Python f-strings use `{}` for interpolation.



















```python









# KILLS YOU:









html = f"var x = {{}}"          # becomes var x = {}  ← OK









html = f"var obj = {{Re:150}}"  # becomes var obj = {Re:150}  ← OK









html = f"try {{ }} catch(e){{}}" # nested = CHAOS



















# THE FIX: if JS gets complex → use .format() or string concat, NOT f-string









# OR: keep ALL JS in a separate variable built with regular strings, then inject









```



















### CURSE 2 — The Unicode/CRLF Curse









Windows git CRLF conversion + unicode chars in Python strings = corrupted bytes.



















```python









# KILLS YOU:









# Using · ✓ ✗ λ̃ χ ← → ⬡ directly inside f-strings on Windows









# Git converts LF→CRLF, byte 0xB7 (·) becomes invalid UTF-8 sequence



















# THE FIX: Use ASCII-only in builder .py files









# Instead of · use  .   or  *









# Instead of ✓ use  OK  or  PASS









# Instead of ✗ use  X   or  FAIL









# Instead of λ̃ use  lam  or  lambda1









# Unicode is fine INSIDE the generated HTML (the output) — just not in the .py source









```



















### CURSE 3 — The Multi-Edit Corruption Curse









The multi_edit tool finds strings by exact match including whitespace.









If the file has CRLF corruption — the string won't match. Ever.



















```









# KILLS YOU:









# Trying to multi_edit a file that has unicode corruption









# The old_string will never match → all edits fail → file untouched









# Then you try again → same failure → 2 attempts wasted



















# THE FIX: If multi_edit fails twice on same file → REWRITE THE FILE CLEAN









# Use create_new_file to replace it entirely









# Never patch a corrupted file — delete and recreate









```



















### CURSE 4 — The f-string Nesting Curse









f-strings cannot contain `\` in expressions. Nested quotes cause SyntaxError.



















```python









# KILLS YOU:









html = f"""









  el.innerHTML = rows.map(function(r){{









    return '<div class=\"dp-row\">' + r[0] + '</div>';  # ← \n in f-string = DEATH









  }}).join('');









"""



















# THE FIX: Build JS glue as regular string, then concat









JS_GLUE = '''









  el.innerHTML = rows.map(function(r) {









    return '<div class="dp-row">' + r[0] + '</div>';









  }).join('');









'''









html = SHELL + "<script>" + JS_GLUE + "</script>" + CLOSE









```



















---



















## THE 3 SAFE PATTERNS



















### PATTERN 1 — Template + Inject (safest)









```python









# Read an existing HTML file as template









# Find the seam (e.g. </script> before </body>)









# Inject new <script> blocks AFTER all existing scripts









# Never modify the template's existing JS



















src = TEMPLATE.read_text(encoding="utf-8")









inject = "<script>\n" + M2 + "\n" + M3 + "\n" + GLUE_JS + "\n</script>"









out = src.replace("</body></html>", inject + "\n</body></html>")









```



















### PATTERN 2 — Separate Variables (for complex JS)









```python









# Build CSS, HTML shell, and JS SEPARATELY as plain strings









# Only use f-string for simple version/timestamp substitutions at the END



















CSS = """..."""           # plain string, no f









HTML_SHELL = """..."""    # plain string, no f









JS_MODULES = M1 + M2     # plain concat









JS_GLUE = """..."""       # plain string, no f — ASCII ONLY



















# Only ONE f-string at the very end to stamp version/date:









final = f"""<!DOCTYPE html>









<title>ENG {VERSION}</title>









<style>{CSS}</style>









{HTML_SHELL}









<script>{JS_MODULES}</script>









<script>{JS_GLUE}</script>









</body></html>"""









```



















### PATTERN 3 — Write with explicit encoding (always)









```python









# ALWAYS write with utf-8 and no BOM









OUT.write_text(html, encoding="utf-8")



















# NEVER use open(OUT, 'w') without encoding= 









# Windows default encoding (cp1252) will destroy unicode in output









```



















---



















## THE RECOVERY PROTOCOL



















When the builder breaks:



















```









1. STOP — do not patch, do not multi_edit a second time









2. READ this file









3. Identify which CURSE hit you (usually Curse 1 or 2)









4. CREATE NEW FILE — clean rewrite, ASCII-only, Pattern 2









5. Run it — verify output









6. ONLY THEN commit









```



















---



















## WHAT IS SAFE TO PUT IN AN f-STRING



















```python









# SAFE — simple substitutions only:









f"<title>ENG {VERSION}</title>"









f"// Built: {TIMESTAMP}"









f"console.log('ENG {VERSION} loaded');"









f"git:{GIT}"



















# NOT SAFE:









f"var x = {{}}"              # OK actually — but avoid nesting









f"function fn(){{ {JS} }}"   # JS variable inside f-string braces = CHAOS









f"color:#{hex_color}"        # # is fine but be careful









f"'\u00b7'"                  # unicode escape in f-string on Windows = CRLF death









```



















---



















## THE KERNEL MODULE INJECT ORDER (never change this)



















```









M1  goldberg_kernel.js   → GK       (always first — everything depends on it)









M2  graph_axioms.js      → GA       (depends on GK)









M3  sar_modular.js       → SAR      (depends on GK)









M4  ns_spectral.js       → NSS      (depends on GK)









M5  fractal_search.js    → FS       (depends on GK + SAR)









M6  mnet_nanite.js       → MNetNanite (depends on GK)









M7  math_tree            → (standalone, inject last, wrap in try/catch)









GLUE                     → always LAST, after all modules









```



















---



















## THE DATA PANEL PATTERN (for eng dashboard)



















When adding live data panels from modules, do it in JS only — no Python generation:



















```javascript









// In GLUE JS (plain string, not f-string):









var PC = {cyan:"#00d4ff", green:"#00ffd5", pink:"#ff69b4",









          gold:"#ffd700", orange:"#ff9040", dim:"#1a2a3a"};



















function setPanel(id, rows) {









  var el = document.getElementById('dp-' + id);









  if (!el) return;









  el.innerHTML = rows.map(function(r) {









    return '<div class="dp-row"><span class="dp-k">' + r[0] +









           '</span><span class="dp-v" style="color:' +









           (PC[r[2]] || '#aaa') + '">' + r[1] + '</span></div>';









  }).join('');









}



















window.addEventListener('load', function() {









  // GK









  var gk = GK.buildC60();









  var inv = GK.invariants(gk);









  setPanel('gk', [









    ['V', inv.vertices, 'cyan'],









    ['P', inv.pents, 'pink'],









    ['chi', inv.vertices - inv.edges + inv.faces, 'gold']









  ]);









  // ... same for SAR, NSS, FS, NAN









});









```



















HTML side — just empty divs:









```html









<div id="dp-gk" class="data-panel"></div>









<div id="dp-sar" class="data-panel"></div>









```



















---



















## CURSE 5 — The File Too Long Curse









Builder scripts get long. create_new_file times out on large files.



















```









FIX: 









  1. create_new_file with empty content first









  2. Output the file content in chunks as code blocks in chat









  3. Vlad pastes each chunk into the file manually









  4. Run + verify









  Never write >200 lines in one create_new_file call









```



















---



















## CURSE 6 -- The File:// Curse









We build locally. We open with file://. We see it differently than the world.









GitHub Pages serves the REAL version. file:// is a lie.



















```









FIX:









  NEVER open with file:// to verify a build.









  ALWAYS open the live GitHub Pages URL:









  https://vsavytsk1.github.io/Mnetv1/shell/FILENAME.html



















  In every builder script the open command must be:









  Start-Process brave "https://vsavytsk1.github.io/Mnetv1/..."









  NOT:









  Start-Process brave "file:///C:/Users/..."



















  The math_tree works because we opened its URL.









  VALE exists at its URL. We just never looked.









```



















---



















## THE DASHBOARD DEVELOPMENT RULE









When building a new dashboard visual or theme -- TWO TABS always:



















```









TAB 1 -- current FULL working dashboard (ENG v2.0 or latest)









         https://vsavytsk1.github.io/Mnetv1/shell/eng_v2.0.html









         This is the reference. Always alive. Always clickable.









         You can summon any module from here while you work.



















TAB 2 -- the visual you are actively building









         https://vsavytsk1.github.io/Mnetv1/shell/vale_v1.1.html









         Only the new thing. Nothing else.



















WHY:









  The new visual is incomplete until fully integrated.









  You need the working dashboard to access modules during dev.









  You need the new visual isolated to see it clearly.









  Never develop blind -- always have the working version open.



















WHEN IS IT FULLY INTEGRATED:









  When the new visual is added as a card in ENG dashboard.









  When it can be summoned from ENG via the overlay.









  When it is in the LEDGER.









  Only then close TAB 1.









```



















---



















## CURSE 7 -- The Black Iframe Mystery (blackMcMistry)









When summonig a full-canvas module inside an iframe it shows BLACK.









This is NOT a CSS issue. NOT a sandbox issue. NOT a GitHub Pages issue.



















```









ROOT CAUSE:









  The tree (math_tree_v4.3 / v5.0) calls center() INLINE at script end:









    drawGridEmpty(); center();



















  center() = panX = (window.innerWidth/2/zm) - CX  where CX = 2000



















  When called inside an iframe at load time:









    window.innerWidth = 0  (iframe layout not finalized yet)









    panX = (0/2/0.6) - 2000 = -2000px









    plane div renders at left:-2000px -- off screen -- BLACK.



















  The EXACT same code works fine in a full tab because









  window.innerWidth is the real viewport width.



















WHAT WE TRIED (all failed):









  1. sandbox attribute -- allow-scripts allow-same-origin etc.









     Result: still black. Wrong diagnosis.









  2. allow=fullscreen on iframe









     Result: still black. Wrong diagnosis.









  3. Loading v5.0 instead of v4.3









     Result: same black. Version was not the issue.









  4. Dispatching resize event to iframe contentWindow









     Result: blocked by sandbox + CORS complexity.



















WHAT WORKED:









  window.open(LINKS[key], _blank)  -- open tree in NEW TAB









  The tree gets a real viewport. center() fires correctly.









  The tree renders. The user sees it.



















THE RULE:









  Any module that calls center() or uses window.innerWidth









  at script-load time (not in a load/resize event) CANNOT









  be summoned in an iframe. It MUST open in a new tab.



















  Modules safe for iframe:









    -- pure data panels (no canvas pan/zoom)









    -- modules that init canvas in window.addEventListener(load)









    -- modules with ResizeObserver for canvas sizing



















  Modules that need new tab:









    -- math_tree (center() inline)









    -- graph_sandbox (pan/zoom canvas init inline)









    -- any module with   drawX(); center();  at script end



















DETECTION PATTERN:









  grep for these patterns at END of script (outside event listeners):









    center()  drawGrid()  drawGridEmpty()  panX =  panY =









  If found at top level -- new tab required.









```



















---



















## CURSE 8 -- The allow-top-navigation Curse









Adding allow-top-navigation to iframe sandbox lets the iframe HIJACK the parent page.









Any link, redirect, or window.location in the summoned module navigates the parent.









The user loses the dashboard. No BACK button can save them. The page is gone.



















```









SYMPTOM:









  User clicks a module card in ENG.









  Module loads in iframe overlay.









  Something in the module triggers navigation.









  ENG dashboard disappears. User is now on the module URL.









  BACK button in browser goes to previous site, not ENG.



















ROOT CAUSE:









  sandbox="allow-top-navigation"









  This grants the iframe permission to set window.top.location.









  Any link with target=_top, any window.location= in module JS,









  any form submit = parent page hijacked.



















FIX:









  Remove allow-top-navigation from sandbox. Always.









  sandbox="allow-scripts allow-same-origin allow-forms allow-popups"









  allow-popups is enough for any external links (they open new tab).









  The parent page is now inviolable.



















RULE:









  iframe sandbox NEVER gets allow-top-navigation.









  If a module needs to navigate: use allow-popups (new tab).









  The dashboard is the god context. Nothing inside can touch it.









```



















---



















## FAILURE LOG



















| Date | File | Curse | What happened | Fix |









|------|------|-------|---------------|-----|









| 2026-05-28 | build_eng_v2.py | Curse 2 | unicode · in f-string → CRLF → UnicodeDecodeError on LEDGER.md read | errors='ignore' |









| 2026-05-28 | build_eng_v2.py | Curse 1+2 | JS {{}} + unicode in f-string → SyntaxError f-string empty expression | Rewrite needed |









| 2026-05-28 | build_eng_v2.py | Curse 3 | multi_edit failed — corrupted file, string not found | Full rewrite |



















---



















*"Each time we touch the builder, black magic is summoned"*









*"More modules = more black magic required"*









*Buenos Aires · May 2026*



















---



















## CURSE 9 -- The 12-Second LCP (Heavy Kernel Load)



















ENG v2.0 loads 6 kernel modules synchronously on page load.









LCP = 12.01s measured in Chrome DevTools.









This is NOT a bug. It is expected behavior.



















```









ROOT CAUSE:









  6 kernel modules load and RUN on window load event:









    M1 goldberg_kernel.js    -- builds C60, runs invariants









    M2 graph_axioms.js       -- runs P1-P7 axiom checks









    M3 sar_modular.js        -- computes lam=0.1473 spectral proof









    M4 ns_spectral.js        -- runs NS flow spectral gap









    M5 fractal_search.js     -- runs fractal architecture search









    M6 mnet_nanite.js        -- builds cluster DAG









  All synchronous. All heavy. All correct.









  LCP fires when the largest element paints = after all 6 run.









  12s on first load. Sub-second on cached repeat.



















WHAT IS NOT THE PROBLEM:









  Not a network issue (GitHub Pages CDN is fast)









  Not a code bug (everything runs correctly)









  Not a render issue (CLS=0, INP=32ms -- excellent)



















WHAT TO DO:









  Accept it. This is a research tool, not a landing page.









  The 12s is the price of having 6 live kernel modules.









  Future optimization: Web Workers for heavy modules.









  But not now. Math first. Performance later.



















HOW TO EXPLAIN IT:









  "LCP 12s because 6 physics modules compute on load.









   Same reason a Jupyter notebook takes 10s to start.









   The computation is the feature."



















SMALL MODULES (obsidius, valtium, etc) load instantly.









Only ENG v2.0 (the full kernel) has the 12s LCP.









Document this in LEDGER when questioned.









```


















---

















## CURSE 10 -- The Shared Pop-Up Lock (blackModuleMystry)

















When a new-tab module opens a popup window,








ALL other modules inherit the popup state.








Subsequent clicks on other modules think THEY








are the popup module and lock the entire dashboard.

















```








SYMPTOM:








  Click sandbox (opens new tab) -> OK








  Go BACK to dashboard








  Click second module -> popup appears (wrong!)








  Click third module -> locked, nothing happens








  Reload page -> vale loads fine in iframe








  








  The popup open/close state is SHARED








  across all module summon() calls.








  Every module thinks it is the one that popped.

















ROOT CAUSE:








  summon() checks NEW_TAB_MODULES dict.








  When popup opens, fr.srcdoc is set.








  The overlay stays OPEN with srcdoc content.








  Next summon() call:








    fr.src = ''  (clears iframe)








    overlay already open = logic confused








    NEW_TAB_MODULES check fires again








    sets srcdoc AGAIN even for non-popup modules








    ALL modules now show portal placeholder








    








  The overlay open state + srcdoc state








  are not reset between summons.








  They bleed into the next call.

















FIX:








  In overlayClose():








    fr.srcdoc = ''    <- clear srcdoc on close








    fr.src = ''       <- already done








    








  In summon() before NEW_TAB_MODULES check:








    if overlay already open -> close first








    reset ALL iframe state








    THEN decide: new tab or iframe








    








  Add a flag: isPopupOpen = false








  Set true when new tab opens








  Reset in overlayClose()








  Check in summon() before proceeding

















THE RULE:








  New-tab modules MUST reset ALL overlay state.








  srcdoc, src, isPopupOpen flag.








  The overlay is not a toggle. It is a state machine.








  Each summon() must start from clean state.








```

















**Curse count: 10. All documented. All slain (eventually).**








**Black magic respects the scroll.**
















---















## CURSE 11 -- The srcdoc Origin Lock (about:srcdoc freeze)















The portal placeholder uses fr.srcdoc to show "LAUNCHED IN NEW TAB".







srcdoc creates an about:srcdoc document inside the iframe.







This is a DIFFERENT ORIGIN from the parent page.







On next summon(), the browser blocks cross-origin iframe access.







The overlay state machine freezes trying to communicate







with the about:srcdoc document.















```







SYMPTOM:







  Fresh load: all modules work perfectly







  Click SANDBOX or TREE (new tab + srcdoc portal shown)







  Go BACK to dashboard







  Click ANY other module:







    IF srcdoc still in iframe -> freeze







    IF reloaded fresh -> works fine







    







  Two sessions behave differently:







    Session A (fresh):    all work







    Session B (post-tab): locks after new-tab module















ROOT CAUSE:







  fr.srcdoc = '<html>...' sets about:srcdoc as iframe src







  about:srcdoc is cross-origin to parent page







  Browser security: cannot access cross-origin iframe







  fr.onload fires but fr.contentWindow = blocked







  Next summon() tries fr.src = '' on cross-origin frame







  Browser throws silent security exception







  Overlay never resets properly







  All subsequent summons: dead















FIX:







  NEVER use srcdoc for the portal placeholder.







  Instead: use a real URL that we control.







  







  Option A: create shell/portal.html







    Tiny file. Shows "LAUNCHED IN NEW TAB" + arrow.







    Served from same origin as ENG.







    No cross-origin issues. Ever.







    







  Option B: use about:blank







    fr.src = 'about:blank' before summon







    about:blank is same-origin-ish







    Safer than srcdoc.







    







  CHOSEN: Option A (portal.html)







  One tiny file. Zero cross-origin issues.







  Same aesthetic. Full control.







  







THE RULE:







  NEVER set srcdoc in production iframe code.







  srcdoc = about:srcdoc = cross-origin = freeze.







  Always use a real URL from the same domain.







  Even for placeholder content.







  Especially for placeholder content.







```















**Curse count: 11. The srcdoc was the demon. portal.html is the counter-hex.**














---













## CURSE 12 -- The Corkscrew Parasite (insideDizzy)













When entering inside view with cam.rx != 0:






  cam.ry += cam.spin  (horizontal rotation)






  cam.rx = 0.3        (fixed pitch tilt)






  RESULT: corkscrew motion. Viewer feels dizzy.






  WE are spinning, not the sphere.













```






ROOT CAUSE:






  cam.rx tilt + cam.ry spin = helical path






  From outside: looks like a nice angled rotation






  From inside:  looks like the whole room corkscrewing






  The camera is TILTED and SPINNING simultaneously.






  The monkey brain reads this as: I AM MOVING.













FIX:






  In inside mode:






    cam.rx = 0  on ENTER (look straight at equator)






    cam.rx = 0  every frame in animate() (lock it)






    only cam.ry spins






    






  Result: sphere faces pass by HORIZONTALLY






  like a panorama rotating past a fixed observer.






  The monkey brain reads this as: THE SPHERE is moving.






  Correct. Comfortable. Fracyclic.













CODE:






  animate():






    if(!dragging) {






      cam.ry += cam.spin;






      if(_insideMode) cam.rx = 0;  // kill the parasite






    }






    






  toggleInsideView() ENTER:






    cam.rx = 0;  // not 0.3 -- that was the parasite













THE RULE:






  Inside view = lock pitch (rx = 0).






  Only yaw (ry) rotates.






  This is also the VR rule:






    in Quest 3, head rotation handles rx.






    auto-spin should never touch rx.






    Only ry (horizontal orbit) auto-spins.






```













**Curse count: 12. The corkscrew is dead.**












---











## CURSE 13 -- The Ghost Spinner (spinnerEgo)











The SPIN slider starts at value="5" (cam.spin=0.005).





You drag it to 0. It shows 0.000.





The sphere keeps spinning.











ROOT CAUSE (three heads):











  HEAD 1: value="5" not value="0"





    Slider starts spinning. Nobody asked for that.





    Developer thought "a little spin looks nice".





    User cannot find zero. Ego. Haunts forever.











  HEAD 2: floating point





    cam.spin = 0/1000 = 0.0





    BUT JavaScript 0.0 is sometimes not exactly 0.





    cam.ry += 0.0 still ticks on some engines.





    Fix: if(Math.abs(cam.spin) > 0.00001) only then add.











  HEAD 3: inside mode sets cam.spin = 0.0008





    This maps to slider value = 0.8 (rounds to 0 visually)





    Slider shows "0.000" but spin is NOT zero.





    User confused. Thinks they stopped it.





    They have not stopped it.











```





FIX:





  1. Slider starts at value="0" (no ego spin on load)





  2. Slider oninput: if value < 1 -> snap to exact 0





     var sv = +this.value;





     cam.spin = sv < 1 ? 0 : sv/1000;





  3. animate(): float zero guard





     if(Math.abs(cam.spin) > 0.00001) cam.ry += cam.spin;





  4. inside mode: cam.spin = 0.001 (visible on slider as 1)





     slider updates to show 1 so user can see and control it











THE RULE:





  Default spin = 0. Always.





  Motion is opt-in, not opt-out.





  The user starts still. They choose to move.





  The ego of "a little spin looks nice on load"





  is the enemy of user control.





  





  This is also the VR rule:





  In Quest 3: start still. Motion sickness kills apps.





  Auto-spin = nausea. Still start = comfort.





  Let the user orbit with their head/hand.





  Only spin on explicit request.





```











**Curse count: 13. The ghost spinner is dead.**





**It came back to haunt us. We knew. We fixed it.**





**Ego = ghost. Documentation = exorcism.**















---









## CURSE 14 -- The CR Accumulator (gitiumCurse)









Repeated Python patch scripts on a Windows HTML file




accumulate carriage returns.









```




ROOT CAUSE:




  File on disk: CRLF line endings (Windows)




  Python reads with errors="ignore"




  Each patch: read -> modify -> write




  




  Problem: some patches use raw string replacement




  that matches \n but the file has \r\n




  When write happens: \r\n + \n = \r\r\n




  Next patch: \r\r\n + \n = \r\r\r\n




  4 patches later: 4 carriage returns per line




  File: 175KB instead of 158KB




  All searches fail (wrong whitespace)




  File is garbage.









HOW TO DETECT:




  raw.count(b"\r") != raw.count(b"\r\n")




  lone CRs > 0 = CURSED









HOW TO FIX:




  git checkout <last_clean_commit> -- shell/file.html




  Verify: lone CRs = 0




  Then re-apply ALL patches in ONE script.









THE RULE:




  DO NOT apply patches incrementally to HTML files.




  Write ONE clean script that does ALL changes.




  Run once. Verify. Commit. Done.




  




  BEFORE any patch script:




    raw = SRC.read_bytes()




    src = raw.decode("utf-8", errors="ignore")




    src = src.replace("\r\n", "\n")  <- NORMALIZE FIRST




    ... do all patches on normalized src ...




    SRC.write_bytes(src.encode("utf-8"))  <- write as UTF-8 no BOM









  This is KERNELIMAGIC PATTERN 3:




    normalize line endings first




    patch on clean \n-only string




    write back as UTF-8




    one script, all patches, run once









PATTERN 3 -- Normalize Then Patch:




  src = SRC.read_bytes().decode("utf-8", errors="ignore")




  src = src.replace("\r\n", "\n").replace("\r", "\n")




  # ... all patches here on clean src ...




  SRC.write_text(src, encoding="utf-8", newline="\n")









This is now the law.




The CR accumulator is documented.




The git restore is the counter-hex.




```









**Curse count: 14. The CR accumulator is named.**




**git checkout is the exorcism.**




**PATTERN 3 is the prevention.**












---







## CURSE 15 -- The Invisible Sort (sortGhost)







sorted.sort() appears to work.



The string is found in the file.



The patch reports OK.



The sort is WRONG.







```



ROOT CAUSE:



  The sort line in genesis_v8.1.html



  was ALREADY patched by a previous



  surviving script run.



  



  Current file contains:



    sorted.sort(function(a,b){



      return _insideMode ? b.depth-a.depth



                         : a.depth-b.depth;



    });



    



  Patch script looks for:



    sorted.sort(function(a,b){return a.depth-b.depth});



    



  NOT FOUND. Patch reports FAIL.



  But the sort IS already correct.



  The FAIL was a false negative.







THE LESSON:



  Before patching: CHECK what is already there.



  A FAIL on patch != the file is wrong.



  A FAIL on patch = the old string not found.



  Could mean: already patched. Or broken. Or different.



  



  ALWAYS verify the INTENT not just the patch result:



    check = "_insideMode?b.depth" in src



    if check: print("SORT ALREADY CORRECT -- skip")



    else: apply patch







PATTERN 3 ADDENDUM:



  After all patches run:



  verify INTENT (what should be true)



  not just patch success (was old string found).



  



  results["P8 sort intent"] = "_insideMode?b.depth" in src



  OR



  results["P8 sort intent"] = "_insideMode ? b.depth" in src







CURRENT STATE of sort:



  sorted.sort(function(a,b){



    return _insideMode ? b.depth-a.depth : a.depth-b.depth;



  });



  CORRECT. No patch needed.



```







**Curse count: 15. The invisible sort. False negative.**



**The file was right. The patch string was wrong.**



**Check intent. Not just patch success.**









---





## CURSE 16 -- The Shadow Duplicate (shadowInject)





Pattern 1 injects JS before last </script>.


The base file ALREADY contains the JS from a previous session.


Inject runs again = TWO copies of same function.


Two var _insideMode. Two toggleInsideView.


JavaScript: last declaration wins.


But BOTH run. State is split. Ghost behavior.





```


ROOT CAUSE:


  Session 1: inject toggleInsideView into genesis_v8.1.html


  Commit. Push.


  


  Session 2: restore to ae55ac4 (already has the injection)


  Run inject script again.


  NOW: TWO toggleInsideView in file.


  TWO var _insideMode.


  The second one overwrites the first at parse time.


  But event handlers bound to first function.


  Chaos.





DETECTION:


  ALWAYS check before injecting:


    count = src.count("function toggleInsideView")


    if count > 0:


      print("ALREADY EXISTS -- replace, do not append")


      


THE RULE:


  Before Pattern 1 inject:


  Check if the target function already exists.


  If yes: REPLACE it, not append.


  


  if "function toggleInsideView" in src:


    # replace existing


    src = re.sub(r'var _insideMode.*?^}',


                 NEW_JS, src,


                 flags=re.DOTALL|re.MULTILINE)


  else:


    # safe to inject at end


    src = src[:last] + NEW_JS + src[last:]





PATTERN 1 ADDENDUM:


  Check for existing before inject.


  Replace if found. Append only if new.


  


THE CORRECT BASE for inside-view work:


  git checkout ae55ac4 -- shell/genesis_v8.1.html


  This base ALREADY has toggleInsideView (from previous session).


  DO NOT inject again.


  ONLY patch the existing function via string replace.


```





**Curse count: 16. The shadow duplicate.**


**The base already had the injection.**


**Replace, do not append.**






---



## CURSE 17 -- The Block Eater (regexDevour)



re.search finds a block.

block_start = 6387

block_end   = 144409

Replace block with new content.

File shrinks from 158KB to 11KB.



```

ROOT CAUSE:

  The regex matched from position 6387

  all the way to the LAST cx.restore();}

  in the ENTIRE file.

  

  The file has many cx.restore(); calls.

  The greedy .* ate everything between

  the inside view block start

  and the LAST restore() in the file.

  

  src[:6387] + NEW_BLOCK + src[144409:]

  src[144409:] = only the last 14KB of file

  src[:6387]   = only first 6KB

  Everything in between: EATEN.



THE FIX:

  NEVER use greedy regex to find block end.

  NEVER replace large blocks of HTML.

  

  Instead: ONLY replace the specific function text.

  Find the exact function string.

  Replace ONLY that string.

  Nothing more. Nothing less.

  

  PATTERN 3 ADDENDUM 2:

    Do NOT find block by start+end regex.

    Find the EXACT string you want to change.

    If string is too long to match: split into parts.

    Replace each part separately.

    

  The safest replace for functions:

    OLD = "function toggleInsideView() {

  var btn..."

    NEW = "function toggleInsideView() {

  var btn..."

    src = src.replace(OLD, NEW)

    assert src.count("function toggleInsideView") == 1



THE RECOVERY:

  git checkout ae55ac4 -- shell/genesis_v8.1.html

  Always. Every time. Do not cry. Just restore.

  The scroll protects the cave.

```



**Curse count: 17. The block eater.**

**Greedy regex devoured 133KB of the file.**

**git restore is always the answer.**

**Replace functions by exact string. Never by regex block.**



---

# THE LOST SAGE BOOK
## Chapter: From Ping to Pixel
## How the MachineNet Kernel Actually Loads
## Written for the curious reader who finds this later.
## And for Unity. This is also the Unity guide.

---

## THE STARTUP SEQUENCE (what actually happens)

When a user hits the URL, this chain fires:

```
1. DNS ping      github.io -> IP            ~10ms
2. TCP handshake browser -> server          ~20ms
3. TLS           secure channel             ~10ms
4. HTTP GET      eng_v2.0.html (142KB)      ~50ms
5. HTML parse    browser reads DOM          ~5ms
6. CSS parse     styles applied             ~2ms
7. JS execute    6 kernel modules load      ~200-12000ms (Curse 9)
8. Canvas init   WebGL context              ~5ms
9. First paint   LCP event fires            measured
10. User sees    the dashboard              DONE
```

Step 7 is where the magic and the curses live.
Everything else is standard web. Boring. Fast.

---

## THE MODULE LOAD ORDER (sacred, never change)

```
M1  goldberg_kernel.js   -> GK    (21KB) ALWAYS FIRST
    defines: PHI, buildC60(), refine(), invariants()
    everything depends on this. touch it = death.

M2  graph_axioms.js      -> GA    (13KB)
    depends on: GK
    defines: GA.P1_node(), GA.edge(), GA.axiomCheck()

M3  sar_modular.js       -> SAR   (27KB)
    depends on: GK
    defines: SAR.buildM0(), SAR.ETA, SAR.verify()

M4  ns_spectral.js       -> NSS   (13KB)
    depends on: GK
    defines: NSS.step(), NSS.residual(), NSS.lam1()

M5  fractal_search.js    -> FS    (13KB)
    depends on: GK + SAR
    defines: FS.search(), FS.locked, FS.bestL

M6  mnet_nanite.js       -> MNetNa (24KB)
    depends on: ALL above
    defines: MNetNa.render(), LOD system

TOTAL: ~111KB of kernel JS
LOAD TIME: 200ms (cached) to 12s (first load, Curse 9)
```

---

## THE PERMUTATION PROBLEM (why we test ALL modules)

We have N modules. Each module:
  - loads its own JS
  - uses iframe or new tab
  - may share state with ENG overlay
  - may trigger Curses 7-11

When you add Module N+1:
  You must test ALL N+1 modules.
  Not just the new one.

WHY:
```
Module A works alone.         ?
Module B works alone.         ?
Module A then Module B:       ? or CURSE 10
Module B then Module A:       ? or CURSE 10 variant
Module C (new tab):
  then Module A:              ? or CURSE 11
  then Module B:              ? or CURSE 11 variant
  
With 10 modules:
  permutations = 10! = 3,628,800
  
  We don't test all permutations.
  We test the CRITICAL PATHS:
    1. Fresh load -> click each module -> BACK -> next
    2. Click new-tab module -> BACK -> click iframe module
    3. Click new-tab module -> BACK -> click another new-tab
    4. Rapid click (stress test)
    5. Click inside view -> EXIT -> click any module
```

---

## THE COLOR PIPELINE (from float to pixel, the lost chapter)

A color in the kernel starts as omega (NS vorticity):
  omega = [-1.0, +1.0] float64

```
STEP 1: omega -> RGB (omegaToColor)
  tanh(omega * 5) -> v in [-1, 1]
  v > 0: rgb(v*80, 200+v*55, 255-v*155) = cyan to blue
  v < 0: rgb(-v*160, 200+v*140, 255) = red to blue
  
  This is 3 multiplications. 3 additions.
  Not a lookup table.
  Not a 45GB color engine.
  Just math.

STEP 2: RGB -> CSS string
  'rgba(' + r + ',' + g + ',' + b + ',' + alpha + ')'
  
  THIS IS THE JAVIUM TOWER.
  This string. This single string.
  
  JavaScript engines (V8 = Chrome, SpiderMonkey = Firefox):
  String concatenation allocates memory.
  Every frame. Every face. Every color.
  At L6 (1.1M faces): 1.1M string allocations per frame.
  At 60fps: 66M string allocations per second.
  V8 has a string intern cache but it's not infinite.
  
  IF YOU TOUCH THIS PATTERN:
    The GC (garbage collector) will notice.
    GC pause = frame drop.
    Frame drop = jank.
    Jank = unhappy monkey brain.
    
  IF YOU NEED TO CHANGE COLOR FORMAT:
    Use a lookup table. Pre-compute strings.
    Or use ImageData (raw pixels, no string).
    But honestly: just leave it. It works.
    The kernel commits sepuku if disturbed.

STEP 3: CSS string -> Canvas pixel
  ctx.fillStyle = colorString
  ctx.fill()
  
  Canvas 2D converts CSS string -> {r,g,b,a} internally.
  This is the browser's job. Not ours.
  
  AT THIS POINT: we are done.
  The color is a pixel on screen.
  Total pipeline: omega float -> 3 math ops -> string -> pixel.
  Simple. Don't touch it.

STEP 4 (Unity path, for later):
  omega float -> Color32(r,g,b,a) struct
  MaterialPropertyBlock.SetColor()
  GPU: vertex shader reads color -> fragment -> pixel
  
  SAME MATH. Same 3 ops. Different host.
  The kernel doesn't care if it runs in a browser or Unity.
  P=12. chi=2. The color is the color.
```

---

## THE STARTUP PERMUTATION TEST (the ritual)

Every time we push a new build:

```
RITUAL:
  1. Open ONE tab. ONE URL.
     https://vsavytsk1.github.io/Mnetv1/shell/eng_v2.0.html
     
  2. Wait for: ALL OK -- 6/6 modules ran
     (bottom right of session log)
     
  3. Click GENESIS -> wait for load -> BACK
  4. Click SANDBOX -> new tab opens -> BACK to ENG
  5. Click any iframe module (HOLLY7, NAVIER, etc)
     -> must load in iframe -> BACK
  6. Click SANDBOX again -> BACK
  7. Click iframe module -> must STILL load (Curse 10/11 test)
  8. Click ENTER in GENESIS -> inside view -> EXIT
  9. Click any module after EXIT -> must still work
  
  IF ALL 9 STEPS PASS: build is clean. ship it.
  IF ANY STEP FAILS: new curse. log it. fix it. repeat.
```

---

## THE UNITY TRANSLATION (same ritual, different host)

When we port to Unity/Quest 3:

```
Step 1 (DNS ping):
  Unity: AssetBundle.LoadFromFile() -> local
  No network. Instant.
  
Step 7 (kernel modules):
  Unity: goldberg_kernel.cs (one file)
  IL2CPP compiled. Native. ~0ms load.
  
Step 9 (first paint):
  Unity: first frame rendered by XR compositor
  Target: <72ms (Quest 3 refresh = 72Hz)
  
THE PERMUTATION TEST becomes:
  1. Launch app
  2. VALE says "yes sir" (kernel loaded)
  3. Click ENTER (inside view)
  4. Sphere wraps around user
  5. Hand tracking: pinch = select face
  6. EXIT: back to menu
  7. All modules accessible from VALE menu
  8. Test all module combos (same ritual)
  
THE COLOR PIPELINE becomes:
  omega -> Color32 -> MaterialPropertyBlock
  Same 3 math ops. GPU handles the rest.
  No string allocations. Pure struct.
  GC doesn't care. Quest 3 happy.
```

---

## THE GOLDEN RULE (for the curious reader)

```
The kernel is not complicated.
It is SIMPLE math applied CONSISTENTLY.

PHI = (1+sqrt(5))/2        <- one constant
buildC60()                 <- one function  
refine(faces, k)           <- one function
invariants(faces)          <- one function
  returns {V, E, F, P, chi, EV}

THAT IS THE ENTIRE KERNEL.
Everything else is rendering.
Everything else is UI.
Everything else is curse management.

The math never fails.
P=12. chi=2. E/V=1.500.
Every refinement. Every frame. Every device.
Browser, Unity, or whatever comes next.

The kernel doesn't know what renders it.
It just returns numbers.
The renderer doesn't know what the numbers mean.
It just draws them.

That is the architecture.
That is why it works.
That is why it will keep working.
```

---

*Lost Sage Book. Chapter: From Ping to Pixel.*
*Written during a session that spawned 17 curses.*
*Buenos Aires. 2026.*
*The scroll grows. The cave is warm.*
*P=12. chi=2. ALWAYS.*


---

## CURSE 18 -- The Windows Devour (windowsDevour)

Python script run via terminal.
Windows sees .py extension.
Opens Notepad instead of executing.
Script never runs. No output. No error. Just Notepad.

```
SYMPTOM:
  Run builder script.
  Notepad opens with source code visible.
  Builder did not execute.
  Nothing changed. Nobody told you.

ROOT CAUSE:
  Windows file association: .py -> Notepad (or similar)
  when Python was not installed as default handler.
  Or: Store version of Python installed but not in PATH.
  run_terminal_command sees "python script.py"
  Windows: "I see .py, I know what to do" -> Notepad.

FIX:
  Use full path to python3.11.exe:
  $py = "C:\Users\vladi\AppData\Local\Microsoft\WindowsApps\python3.11.exe"
  $code = @'...'@
  $code | & $py
  
  Never: python script.py
  Always: & $py script.py  OR  $code | & $py (heredoc)
  
  This is the established protocol throughout the cave.
  It works. It always worked.
  The Notepad was the enemy. The full path is the counter-hex.
```

**Curse count: 18. Notepad was the devour.**
**Full path always. Heredoc always. The Windows PATH is not to be trusted.**


---

## CURSE 19 -- The Shell Devour (shellDevour)

After approximately 44 consecutive tool calls in one session,
the run_terminal_command tool begins returning empty results.
No error. No output. Just silence.

```
SYMPTOM:
  Commands that work fine early in session.
  After 40+ calls: same commands return nothing.
  No error message. Just empty output.
  Builder appears to run but produces nothing.
  git status returns nothing.
  File writes appear to succeed but file unchanged.

ROOT CAUSE:
  The IDE shell (Continue / VS Code integrated terminal)
  has a maximum command buffer per session.
  After ~44 calls the shell process degrades.
  Tool calls: accepted. Results: eaten.
  The shell is full. It devours silently.

FIX:
  Option A: New session. Fresh shell. Zero count.
  Option B: Use the actual terminal (not IDE shell).
  Option C: Break into fewer, larger operations.
            One heredoc that does all 10 things.
            Not 10 separate calls.
  
THE RULE:
  Batch operations. Always.
  One script that does everything.
  Not 10 scripts that each do one thing.
  This is ALSO why Pattern 3 exists:
    One clean script. All patches. Run once.
    Not 5 patches. 5 calls. 5 risks of shellDevour.
    
  The shell devour is also a DESIGN SIGNAL:
  If you need 44 tool calls to do one thing --
  you are doing it wrong.
  One builder script. One run. One verify. Done.
```

**Curse count: 19. The shell ate the commands.**
**One script. One run. Pattern 3. Always.**


---

## CURSE 20 -- The Camerum (projectCameraDevour)

Inside view camera and sphere faces use the SAME project() function.
Zoom changes both simultaneously.
The camera moves and the faces move with it.
User: sees no change. Thinks nothing happened.
Actually: both transforms applied. Net effect: zero.

```
SYMPTOM:
  Enter inside view.
  Move closer to a face.
  The face appears to stay the same distance.
  Zoom slider: nothing visible changes.
  cam.zoom increases: faces get bigger AND camera
  moves back by the same amount. Net: stationary.

ROOT CAUSE:
  project(p) is ONE function:
    x_screen = W/2 + (rotated_x) * cam.zoom
    
  cam.zoom scales EVERYTHING:
  - sphere face positions (visual)
  - camera position (perspective)
  
  From inside the sphere:
    Increase zoom -> faces look bigger (good)
    But also -> camera pushed back (bad)
    Two transforms cancel. User sees nothing.
    
  From outside: zoom just scales uniformly. Fine.
  From inside: decoupled transforms required.

FIX:
  project_camera(p): uses _surfaceR (camera position)
                     independent of sphere face scale
  project_sphere(p): uses POV angle + sphere radius 1.6
                     independent of camera position
  
  They share cam.rx, cam.ry (rotation).
  They do NOT share scale or origin.
  
  Two functions. Two transforms. One screen.
  The camera is at 5000R from sphere center.
  The sphere faces render at their natural 1.6R.
  POV slider (10-120 deg) controls field of view.
  HEIGHT slider controls camera Y position.
  
  projectCamera() for grid and environment.
  project() for sphere faces.
  Never mix.

THE RULE:
  Inside view = two decoupled transforms.
  Camera space: enormous (5000R).
  Sphere space: natural (1.6R).
  Meeting point: screen pixels. Nothing else shared.
  
  This is also the Unity rule:
    Camera rig: XR Origin transform
    Sphere: separate GameObject
    They share the scene. Not the math.
  
CODE FIXED (L110):
  function projectCamera(p) { ... uses _surfaceR ... }
  function setPOV(deg) { ... FOV control ... }
  Grid and floor: use projectCamera()
  Sphere faces: use project()
```

**Curse count: 20. The camerum coupled what must be free.**
**Two transforms. One screen. Never mix. Always.**

---

*Curse count: 20. All documented. All slain (eventually).*
*The scroll grows as the cave deepens.*
*git restore is always the answer.*
*Pattern 3 is always the protocol.*
*Buenos Aires. 2026.*


---

## CURSE 21 -- The Musiquim Autoplay (browserSilence)

Browser will SILENTLY block audio.autoplay() if user has not interacted with page.
No error. No warning. Just silence. The geometry screams into the void.

```
SYMPTOM:
  audio.play() called on page load.
  Nothing happens.
  No error in console.
  No exception thrown.
  Just: silence.
  
  OR:
  Uncaught (in promise) DOMException:
  play() failed because the user didn't
  interact with the document first.

ROOT CAUSE:
  Chrome/Firefox/Safari autoplay policy (2018+).
  Audio/video autoplay blocked by default.
  REQUIRES a user gesture (click, keypress, touch)
  BEFORE any audio.play() call.
  
  Even if you call audio.play() after page load:
  if no user gesture happened first -> BLOCKED.
  Silently in some browsers. Exception in others.

FIX:
  NEVER autoplay on load.
  ALWAYS require explicit user action.
  
  The correct pattern:
    var audio = new Audio('slimium_toon.mp3');
    audio.loop = true;
    // DO NOT call audio.play() here
    
    // Only play on user gesture:
    btn.addEventListener('click', function() {
      if (audio.paused) audio.play();
      else audio.pause();
    });
  
  KILL SWITCH (one command, as demanded):
    // To disable music globally: set this flag
    var MUSIC_ENABLED = true;  // <- change to false to kill
    // In button handler: if(!MUSIC_ENABLED) return;
    
  THE RULE:
    Audio: opt-in only. Never opt-out.
    Same as spin slider (Curse 13).
    Motion is opt-in. Sound is opt-in.
    The user starts in silence.
    They choose to hear.
    Always.

FILE SIZE RULE:
  Do NOT base64-encode audio into HTML.
  4.8MB mp3 -> 6.5MB base64 -> GitHub ok but terrible UX.
  Copy mp3 to same folder as HTML.
  Reference as relative URL: new Audio('slimium_toon.mp3')
  GitHub Pages serves it from same domain.
  No CORS issues. Clean. Fast.
  
  If mp3 > 50MB: use CDN or external URL.
  Our slimium_toon.mp3: 4.8MB. Fine. Ship it.
```

**Curse count: 21. The browser enforces silence.**
**User gesture required. Opt-in only. Always.**


---

## CURSE 22 -- The Gitium Novicium (newRepoPages404)

New GitHub repo. Files pushed. URL opens. 404.
No error during push. No warning. Just 404 forever.

ROOT CAUSE:
  GitHub Pages is NOT automatically enabled on new repos.
  You must enable it manually in Settings > Pages.
  OR: push a .nojekyll file to trigger Pages detection.
  
  ALSO: the default branch matters.
  GitHub Pages serves from the branch you specify.
  If you pushed to 'master' but Pages expects 'main': 404.
  If you never enabled Pages at all: 404.
  If no .nojekyll and Jekyll fails on your HTML: 404.
  
  The gitium novicium (new repo curse) hits every time
  because it looks like a push problem
  but it is a Settings problem.
  Two completely different places.
  The terminal lies by omission.

FIX (two steps, both required):
  
  STEP 1: Push .nojekyll to root
    echo "" > .nojekyll
    git add .nojekyll
    git commit -m "enable GitHub Pages"
    git push
    
  STEP 2: Enable Pages in GitHub Settings
    Go to: github.com/vsavytsk1/REPONAME/settings/pages
    Source: Deploy from branch
    Branch: master (or main) / root
    Save.
    Wait 2-3 minutes.
    URL: vsavytsk1.github.io/REPONAME/
    
  ALSO CHECK: is the branch 'master' or 'main'?
  New repos default to 'main'.
  Old repos use 'master'.
  GitHub Pages must match the actual branch name.
  
THE RULE:
  Every new repo: .nojekyll on first commit.
  Every new repo: Settings > Pages immediately after.
  Do not assume Pages is enabled.
  It is never enabled automatically.
  The cave has been burned by this before.
  Document it. Never again.
  
  DETECTION: if vsavytsk1.github.io/REPONAME/ gives 404
  and git push was successful: it is ALWAYS this curse.
  Not the code. Not the HTML. Not the kanji.
  Just Pages not enabled.
  Always.

## CURSE 23 -- The Python Leak (pythonInJS)

A Python patch script generates JavaScript.
The script reaches for a Python builtin -- chr(), ord(), len() --
and that builtin lands LITERALLY inside the emitted JS.
Browser console: "chr is not defined". 19 errors. Every click.
Silent during build. The push succeeds. The curse waits for the click.

ROOT CAUSE:
  The patch is written in Python. The output is JavaScript.
  When you type chr(46) thinking "dot", Python does NOT evaluate it --
  it is inside a string literal that becomes JS source.
  JavaScript has no chr(). The boundary between the two languages
  is invisible inside a single string. That seam is where the curse lives.

  lbl.textContent = (start+i+1)+chr(46)+...   <- chr(46) shipped raw
  JS sees chr(46) -> ReferenceError: chr is not defined

FIX:
  Never write Python builtins into JS strings.
  Use literal characters: "." not chr(46), "+" not chr(43).
  If you truly need a char from a code point, build it in Python
  BEFORE it enters the JS string, or use JS String.fromCharCode in JS.

FAMILY:
  Same family as CURSE 1 (Curly Brace) and CURSE 4 (f-string Nesting).
  The language boundary is always the killer.
  Python thinking leaks into JS. JS thinking leaks into Python.
  The seam is invisible until the click.

  DETECTION: console says "X is not defined" where X is a Python builtin
  (chr, ord, len, range, str, int) -- it is ALWAYS this curse.
  Not the logic. Not the data. Just Python wearing a JS coat.
  Always.

## CURSE 24 -- The Cache Lie (staleServe)

You fix the scar. You commit. You push. Pages deploys (green check).
The raw file on the server is HEALED -- verified, byte for byte.
But the browser console STILL screams the old error, same line, same token.
A physicist watches. The error that should not exist... exists.
You begin to doubt the fix. You re-read the scroll for a curse that is gone.

ROOT CAUSE:
  The browser cached the BROKEN file before the fix deployed.
  It serves the corpse, not the cure. The bytes on GitHub are correct;
  the bytes on screen are a screenshot of the past.
  GitHub Pages also sets long cache headers, so the stale copy lingers.
  The console error points at a line that no longer contains the bug.
  You are debugging a ghost.

PROOF (do this before touching ANY code):
  1. Local file line N        -> git show HEAD:file | line N
  2. Committed HEAD line N     -> matches the fix
  3. RAW server bytes line N   -> Invoke-WebRequest <url>?nocache=$(Get-Random)
                                  -Headers @{'Cache-Control'='no-cache'}
  If all three are CLEAN but the browser errors -> it is THIS curse.
  The codebase is not the cache.

FIX:
  The file needs no fix. The browser needs a flush.
    Ctrl+Shift+R        (hard reload)
    incognito / private window
    append ?v=2 (any new query string busts the cache)
  For agents: page.goto(url + '?bust=' + Date.now()), clear cookies/context.

FAMILY:
  Cousin of CURSE 6 (File:// Lie) -- both show bytes that are not the live truth.
  Where Curse 6 lies about WHICH file, Curse 24 lies about WHEN.
  Cousin of CURSE 15 (False Negative) -- the tool/screen reports a failure
  that the file already disproves.

  DETECTION: console error points at a line that, when you read the LIVE
  raw bytes, does NOT contain the reported token. The git is clean, the
  push is green, the raw fetch is clean -- only the rendered tab is wrong.
  It is ALWAYS the cache. Never the codebase. Flush, do not patch.
  Always.

Curse count: 24. The cache is not the codebase. Flush, do not patch. Always.


---

## GLAMOUR 01 -- The Growing Bar (chipBloom)

  Not a curse -- a glamour. A bug so pretty it could be a feature.

  WHAT HAPPENED: the word-by-word stepper appended a kanji-chip per match.
  The chip row was flex-wrap:wrap with no height cap inside a fixed-height
  panel. Each click that added a word added chips; the chips wrapped to new
  lines; the row grew UPWARD and shoved the typed sentence out of view.
  So the bar "ate" your text and "grew" as you clicked -- like a magic
  scroll that gives you more words but hides the ones you wrote.

  WHY IT IS COOL: it accidentally felt like a living, breathing input that
  rewards you with more meaning the more you feed it. Keep this idea on ice:
  a deliberate "meaning bloom" panel that expands (with intent + animation)
  as the sentence graph grows, then settles -- could be a real feature later.

  THE FIX (for now): lock the bar. input-row flex:0 0 auto, match-row
  single-line with horizontal scroll (thin gold bar), panel clips overflow.
  Height stays 110px no matter how many chips. Typed text never hidden.

  FAMILY: cousin of any unbounded flex-wrap inside a fixed-height flex
  parent -- the child wraps and overflows its sibling instead of itself.
  Cap the child or let it scroll; never let it push the bar.

  Glamour count: 1. Some bugs are seeds. Log them, do not just kill them.

---

## CURSE 25 -- The Rune Rot (glyphCorrupt)

You are typing a non-Latin verse into a JS string as \u escapes -- Greek,
Devanagari, Ethiopic, Lao, Georgian, Kannada. Your hand (or the model's hand)
fumbles ONE escape: a space slips in (\u0 AA7), a stray letter (\u0influenced,
\u10late), a half code point (\u12b + a real glyph). The browser cannot decode
it, so it substitutes U+FFFD -- the replacement char. The ring renders, the page
does not error, but one rune is now a black diamond question mark. Ship it and
you have carved GARBAGE into the stone of a language you do not read.

```
SYMPTOM:
  A non-Latin string shows a lone diamond-question-mark, or a glyph that is
  clearly not that script. No JS error. get_errors is clean. The page runs.
  Only the eyes (or a byte scan) catch it.

ROOT CAUSE:
  \uXXXX needs EXACTLY four hex digits, no spaces, no typos. Hand-typing long
  runs of escapes for a script you cannot read = high error rate, invisible.
  A broken escape decodes to U+FFFD (bytes EF BF BD) or eats the next char.

HOW TO DETECT (before commit, always for any non-ASCII add):
  raw = open(f,'rb').read()
  text = raw.decode('utf-8')
  assert '\ufffd' not in text          # U+FFFD present == CURSED
  # and scan for malformed escapes in the SOURCE:
  #   regex \\u[0-9a-fA-F]{0,3}[^0-9a-fA-F"\\]  -> any hit == a broken \u
  # PowerShell one-liner used in the cave:
  #   $t.Contains([char]0xFFFD)   must be False

HOW TO FIX:
  Never fake a script you cannot verify. Two honest options:
    1. Paste a VERIFIED source string (public-domain scripture etc.), or
    2. Fall back to honest romaji/transliteration and MARK it as such.
  A clean transliteration beats a corrupted native glyph. Always.
  (K3 of the language work: coverage may be INCOMPLETE; it must never be FAKE.)

FAMILY:
  Cousin of CURSE 2 (Unicode/CRLF) -- both are byte-level text corruption, but
  Curse 2 is about line endings on write; Curse 25 is about malformed code points
  on authoring. Cousin of CURSE 23 (Python Leak) -- both are the wrong token
  wearing the right costume until something downstream chokes.

  DETECTION RULE: after ANY edit that adds non-ASCII, scan for U+FFFD and for
  malformed \u escapes. Zero, or it does not ship. The center is agapi; the rim
  must be honest. Always.
```

Curse count: 25. Never carve garbage into a tongue you cannot read. Verify or transliterate. Always.

---

## CURSE 26 -- The False Convergence (lockLie)

You build an optimizer with a TARGET (0.7) and a knob (q, a weight, a mean).
The HUD shows the target proudly: "gate 0.700". A "descend -> 0.7" button glows.
But the actual error sits wide open (lock err 0.600) and the knob is somewhere
else entirely (slider says 1.30). Three sources disagree: the displayed target,
the live knob, and the true error. You are SHOWING a lock you never reached.
The compute never paid the price -- but the screen claims the prize.

```
SYMPTOM:
  A "converged / locked / 0.700" readout while the honest error metric is large.
  A manual slider and an auto-descent fighting each other (drag the knob, the
  descent drags it back; the label shows neither). The optimum is DISPLAYED as
  achieved before the descent has actually run to tolerance.

ROOT CAUSE:
  The TARGET constant is printed as if it were the RESULT. The gate weight 0.700
  is our CHOSEN price (a design seed, K4) -- it is NOT proof the system reached it.
  Two controllers (auto-descend + manual knob) write the same variable with no
  single source of truth, so the UI shows a value nothing actually holds.

HOW TO DETECT:
  Show BOTH always, side by side, and never let them lie:
    target      = 0.700   (the chosen price)
    current     = <live>  (what the knob actually is)
    err         = |current - target|   (the unpaid distance)
  If a "locked / converged" badge can be true while err > tol -> CURSED.
  If a manual input and an auto-optimizer both write the knob -> pick ONE owner
  at a time (arming manual DISARMS descent, and the UI must reflect it).

HOW TO FIX:
  1. Never print the target as the result. Print current +/- err, always, with
     the target as a separate reference line. (The gate shows 0.700 as the GOAL;
     the error shows how much compute still owes.)
  2. Single owner for the knob: manual OR descent, never both silently.
  3. A "locked" state is EARNED: badge only when err <= tol, for K frames.
  4. Pay the price honestly: if the descent cannot reach tol at this compute,
     SAY SO (err shown), do not fake the 0.700. 0.7 is impossible exactly; we
     show 0.7 +/- precision and admit the gap. Always.

FAMILY:
  The optimizer's cousin of CURSE 15 (False Negative Sort) and CURSE 24 (Cache
  Lie) -- all three are the SCREEN disagreeing with the TRUTH. Curse 15: the tool
  lies it failed. Curse 24: the tab lies it is old. Curse 26: the HUD lies it won.

  DETECTION RULE: any "target reached / converged / locked / 0.700" claim must be
  gated on the live error being within tolerance. Target != result. The price is
  paid in compute and MEASURED, never assumed. The center is agapi; the receipt
  must be real. Always.
```

Curse count: 26. Never show the prize before the compute pays for it. Target is not result. Always.

---

## CURSE 27 -- The Clone Mirage (originMirage)

You have a repo named JARVIS. It looks like its own project. It is not.
Its `origin` points at a DIFFERENT repo (VALE). Long ago you worked in it,
committed real code -- whisper_window.py, a config line, notes -- and never
pushed. Meanwhile the true VALE repo moved on (two new commits). Now the folder
name lies about what it is, the remote lies about where it belongs, and unique
work sits marooned in a directory nobody thinks to look in. Then a fourth ghost
appears: VALE-main, a plain COPY with no .git at all -- same files, zero history.
Three folders, one project, and the drive quietly rots the truth.

```
SYMPTOM:
  A git sweep shows one repo "diverged": behind=2 ahead=2 (not just behind).
  The folder's name does not match its `git remote get-url origin`.
  Unique files exist in the clone that are absent from the canonical repo.
  A same-named sibling folder is NOT a git repo (plain copy, no .git).
  You cannot tell which of the N folders is the real one from the file tree.

ROOT CAUSE:
  A repo was cloned/copied into a differently-named folder (or the wrong repo
  was cloned into a project-named folder). The working folder name became the
  identity in the human's head; the `origin` remained the real identity in git.
  The two drift apart. Local commits never pushed + upstream commits never pulled
  = divergence. Copies made with the file explorer (not git) strip .git entirely,
  producing history-less twins that look identical on disk. Windows + OneDrive
  sync makes silent duplicates worse ("Folder (1)", "-main", "-git" suffixes).

HOW TO DETECT (run on EVERY local repo, not just the one you are in):
  for each folder:
    name   = Split-Path $folder -Leaf
    origin = git -C $folder remote get-url origin      # does name ~ origin?
    git -C $folder fetch
    git -C $folder rev-list --left-right --count origin/$b...$b   # 0 0 or drift?
    Test-Path (Join-Path $folder ".git")               # false = plain-copy ghost
  A name that disagrees with origin, OR ahead>0 on a clone you forgot, OR a
  .git-less twin -> CURSED.

HOW TO FIX (never destroy unpushed work to tidy up):
  1. IDENTIFY the ONE canonical clone per repo (origin matches intent, synced).
  2. SALVAGE first: diff the marooned unique files against the canonical repo.
     Copy anything worth keeping INTO the canonical clone, commit it there.
  3. Do NOT `git push` the misnamed clone to the shared origin to "sync" it --
     that injects stale/unrelated commits (old exports, dead branches) into the
     real repo. Salvage the files, not the tangled history.
  4. Only after salvage: retire the ghost (delete the misnamed clone and the
     .git-less copy), leaving exactly one folder whose name == its origin.
  5. Confirm with the human before deleting ANY folder -- a marooned clone may
     be in-progress work, not garbage (Axiom 04: honest boundaries).

THE RULE:
  One project = one folder = one clone whose NAME matches its ORIGIN.
  Never copy a repo with the file explorer; always `git clone`.
  A folder's identity is `git remote get-url origin`, never its name on disk.
  Sweep ALL repos for name-vs-origin mismatch, divergence, and .git-less twins.

FAMILY:
  Cousin of CURSE 6 (File:// Lie) and CURSE 24 (Cache Lie) -- all three are the
  drive/screen lying about the live truth. Curse 6 lies about WHICH file, Curse
  24 about WHEN, Curse 27 about WHERE a project really lives. Enforced by
  Galactic Law AXIOM 02 (Absolute Return): every branch returns to main, every
  clone returns to its true origin, or the phantom folders accumulate.

  DETECTION RULE: if `git remote get-url origin` does not match the folder's name
  and purpose, or a sibling copy has no .git -- STOP. Map every clone before you
  trust any of them. The folder name is a mirage. The origin is the truth. Always.
```

Curse count: 27. The folder name is a mirage; the origin is the truth. One project, one clone. Always.
---

## CURSE 28 -- The Wedged Host (hostWedge)

You run a command. The terminal answers `^C` and nothing else. You run it again --
`^C`. No error, no output, no exit. It looks EXACTLY like CURSE 19 (Shell Devour),
so you blame the ~44-call limit and reach for a new session. But the call count is
low and a DIFFERENT terminal in the same window works fine. The truth: your command
routed to the wrong shell host -- the VS Code **PowerShell Extension Integrated
Console (PSES)**, not a plain `pwsh`. PSES got wedged (a half-finished heredoc, a
bracket paste, a debugger prompt, or a Ctrl-C mid-read) and now swallows every line.
The cave has two mouths; you are shouting into the one that is choking.

```
SYMPTOM:
  Every command returns only `^C` (or empty) with exit shown as success/none.
  Reproduces on retry, but a sibling terminal tab runs the same command instantly.
  The stuck tab is usually named "PowerShell Extension" and shows an
  aka.ms/vscode-powershell banner (that is PSES, the Editor Services console).
  Often starts right after an interrupted multi-line paste / heredoc / here-string.

ROOT CAUSE:
  VS Code can host MORE THAN ONE shell:
    - "pwsh" / "PowerShell"      = a normal ConsoleHost (Host.Name = ConsoleHost).
    - "PowerShell Extension"     = PSES Integrated Console (Host.Name =
                                   Visual Studio Code Host), driven by the PS
                                   extension + its language server.
  PSES multiplexes your input with its own protocol traffic. A broken paste or a
  stray Ctrl-C leaves its read loop half-open; subsequent sends are eaten and it
  emits a bare `^C`. The commands are NOT running. Nothing you typed executed.

HOW TO DETECT (one line, run it when output goes quiet):
  Write-Output "HostName=$($Host.Name) PID=$PID"
    ConsoleHost           -> a real pwsh, safe.
    Visual Studio Code Host-> you are in PSES; if it also prints nothing, it is WEDGED.
  A crisp tell: the SAME command returns `^C` in one tab and real output in another.
  This is CURSE 19's twin -- distinguish them: Shell Devour = high call count, ALL
  hosts degrade; Host Wedge = low call count, only the PSES tab is dead.

HOW TO FIX:
  1. Do NOT keep retrying the same wedged host -- it will `^C` forever.
  2. Switch to a plain ConsoleHost: open a new "pwsh" terminal (not the Extension
     one), or select the pwsh tab you already have. Re-run there; it just works.
  3. NEVER paste multi-line heredocs / here-strings into PSES. Per CURSE 18/19 law:
     write a .py or .ps1 file and run it by path (one call), do not paste a block.
  4. If you must revive PSES: "PowerShell: Restart Session" from the command
     palette, or kill that terminal and spawn a fresh one. Cheaper to just use pwsh.
  5. File edits do NOT need the terminal -- use the edit tools; only shell out for
     git / verification, in a KNOWN-GOOD ConsoleHost tab.

FAMILY:
  Twin of CURSE 19 (Shell Devour) -- both give silent/`^C` empty output; Shell
  Devour is the ~44-call session limit (all hosts), Host Wedge is ONE bad host
  (PSES) while others live. Cousin of CURSE 18 (Windows Devour) -- both are "the
  command never actually ran, and nobody told you." The fix rhyme for all three:
  ONE script by path, in a real console, verified after.

  DETECTION RULE: output is only `^C`/empty but a sibling terminal works -> it is
  the host, not your code and not the call count. Print $Host.Name; if it is the
  Visual Studio Code Host and it is silent, abandon it for a plain pwsh. Always.
```

Curse count: 28. Two mouths in the cave; one is choking. Print the host, switch to pwsh, never paste blocks into PSES. Always.

---

## CURSE 29 -- The Eager Verify (deployLag)

You commit. You push. `git push` returns in one second and says everything is fine.
So -- being a fast little goblin -- you IMMEDIATELY open the live URL to admire it.
404. Or the old bytes. Or a `git status` that has not caught up. Your heart drops:
did the push fail? did I break Pages? You start debugging a bug that does not exist.
The truth: `git push` only hands the commit to the remote. GitHub Pages then runs a
SEPARATE `pages-build-deployment` job that takes ~30-90 seconds to actually publish.
Windows/OneDrive filesystem sync lags the same way. The machine is not broken --
it is LAZY, and you were TOO FAST. The build is a step; patience is part of the step.

```
SYMPTOM:
  Push succeeds, but seconds later the live URL 404s or serves the previous version.
  A just-pushed file is "missing" on Pages though it is clearly in origin/main.
  `git status` / a sync indicator briefly disagrees with what you just did.
  Five minutes later, with zero code changes, everything is perfect. Ghost fixed.

ROOT CAUSE:
  Three lazy layers, each with its own clock, none of them instant:
    1. git push       -> uploads the commit; returns immediately (fast).
    2. Pages deploy   -> a queued GitHub Action (pages-build-deployment) builds and
                         publishes. ~30-90s typical, longer if the queue is busy.
    3. CDN + Windows  -> edge cache warm-up + OneDrive/NTFS sync settle after that.
  You measured layer 1 and judged layer 2/3. The prize is not served yet.

HOW TO DETECT (do not guess -- WATCH the pipeline, not the clock):
  - GitHub -> Actions (or repo -> Deployments/Environments): the newest
    pages-build-deployment must show GREEN / "Active" for YOUR commit sha.
    Yellow dot = still building = of course the URL 404s. That is not a bug.
  - Only once it is green is the live URL a fair test.
  - If green + correct sha but the TAB still errors -> now it is CURSE 24 (cache),
    flush the browser. If never green + 404 on a NEW repo -> CURSE 22 (Pages off).

HOW TO FIX:
  1. Push, then WAIT for the deployment to go green before verifying. ~60 seconds
     is the honest human pace here. Do not spam-refresh; watch the Deployments tab.
  2. Do NOT poll in a tight loop or Start-Sleep-hammer the terminal (that is its own
     curse -- see hostWedge/shellDevour). End the beat, let the Action run, come back.
  3. Verify against the deployment sha, not against your hope. Green sha == truth.
  4. Bake the wait into the ritual: commit -> push -> (deployment goes green ~60s)
     -> hard-refresh the live URL -> THEN celebrate. The pause is a build stage.

FAMILY:
  The timing sibling of CURSE 22 (Gitium Novicium: 404 because Pages is OFF) and
  CURSE 24 (Cache Lie: stale because the BROWSER cached). Distinguish the trio:
    - 404 on a NEW repo, never deploys          -> CURSE 22 (enable Pages).
    - 404/stale seconds after push, then heals  -> CURSE 29 (deploy lag, WAIT).
    - correct on server but tab still wrong      -> CURSE 24 (flush cache).
  All three are "the screen is not the truth YET." 22 = where, 29 = WHEN-not-ready,
  24 = when-too-old. Also cousin of the human note: git + Windows 11 are the same
  kind of lazy; the fast agent must slow to the pipeline's pace. Always.

  DETECTION RULE: if a just-pushed change is missing/old on the live URL, CHECK the
  deployment status first. Yellow/queued -> it is this curse: wait ~60s for green,
  do not touch the code. The build has a clock; respect it. Always.
```

Curse count: 29. git push is not deploy. Watch the deployment go green (~60s), then verify. The machine is lazy; do not be fast. Always.