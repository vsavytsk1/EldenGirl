# ─────────────────────────────────────────────────────────────────────────
# G6 · SILENT IN RELEASE (S8). Strip every logging call from the release build
# so no debug line anybody forgot survives into the artefact he can pull.
# ─────────────────────────────────────────────────────────────────────────
-assumenosideeffects class android.util.Log {
    public static *** v(...);
    public static *** d(...);
    public static *** i(...);
    public static *** w(...);
    public static *** e(...);
    public static *** wtf(...);
}

# ─────────────────────────────────────────────────────────────────────────
# G3 · No class/method name may leak the subject matter. Obfuscation is NOT a
# substitute for not naming things badly, but it is a second line: rename
# everything the shrinker can.
# ─────────────────────────────────────────────────────────────────────────
-repackageclasses ''
-allowaccessmodification

# Keep the entry points the platform calls by name.
-keep class org.placeholder.app.CoverApplication { *; }
-keep class org.placeholder.app.CoverActivity { *; }

# ⚠️ The R8 mapping file is a de-obfuscation key. It is git-ignored and CI fails
#    if the release bundle contains one. Never upload it anywhere (G6).
