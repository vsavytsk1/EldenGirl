import java.util.Properties

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

// ─────────────────────────────────────────────────────────────────────────
// COVER IDENTITY IS A BUILD PARAMETER WITH NO DEFAULT (v1.5 Part I, G11).
// The repo carries only "org.placeholder.app" / "PLACEHOLDER". The distributing
// organisation supplies real values through an UNTRACKED cover.properties (see
// .gitignore) or -P flags. If cover.properties is absent, the build uses the
// placeholders — which is correct for CI and for anyone cloning to read the code.
// ─────────────────────────────────────────────────────────────────────────
val cover = Properties().apply {
    val f = rootProject.file("cover.properties")
    if (f.exists()) f.inputStream().use { load(it) }
}
fun coverProp(key: String, fallback: String): String =
    (cover.getProperty(key) ?: project.findProperty(key) as String? ?: fallback)

val coverName: String = coverProp("COVER_NAME", "PLACEHOLDER")
val coverPackage: String = coverProp("COVER_PACKAGE", "org.placeholder.app")

android {
    namespace = "org.placeholder.app"          // source namespace stays placeholder; G11 enforces it
    compileSdk = 35

    defaultConfig {
        applicationId = coverPackage            // real id injected at build time only
        minSdk = 26                             // API 26: IME_FLAG_NO_PERSONALIZED_LEARNING (v1.5 III·1)
        targetSdk = 35
        versionCode = 1
        versionName = "0.1"

        // The cover's visible name is injected, never committed.
        resValue("string", "app_name", coverName)

        // No test runner that phones home; no vector-drawable support lib.
        vectorDrawables { useSupportLibrary = false }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            // G6: strip logging; and DO NOT ship the mapping file (handled in .gitignore + CI).
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    buildFeatures { compose = true }

    // No buildConfig fields that could carry identity or endpoints.
    buildFeatures { buildConfig = false }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }

    // Reproducible builds (THE_APP.md Part III): strip timestamps from the artefact.
    dependenciesInfo {
        includeInApk = false
        includeInBundle = false
    }
}

// ─────────────────────────────────────────────────────────────────────────
// DEPENDENCIES: every line here must also exist in gates/allowed-deps.txt (G2).
// Compose foundation only — no Material library, no networking, no analytics,
// no crash reporter, nothing that reaches the network (S8).
// ─────────────────────────────────────────────────────────────────────────
dependencies {
    implementation("org.jetbrains.kotlin:kotlin-stdlib:2.0.20")
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.activity:activity-compose:1.9.2")
    implementation("androidx.compose.ui:ui:1.7.2")
    implementation("androidx.compose.foundation:foundation:1.7.2")
}
