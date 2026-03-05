/**
 * Portfolio Observability & Telemetry
 * Professional-grade RUM with privacy-first defaults.
 */

(function () {
    // 1. Kill Switch Check (?noai=1)
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('noai') && urlParams.get('noai') === '1') {
        console.warn("[Observability] Telemetry disabled via kill-switch.");
        window.telemetryDisabled = true;
        return;
    }

    // 2. App Insights Connection String
    // [PROD READY] - Using provided instrumentation key from user configuration
    const connectionString = "InstrumentationKey=8fc596f2-bb91-49d7-8495-2ac1ecd30501;IngestionEndpoint=https://centralindia-0.in.liana.ice.azure.microsoft.com/";

    if (!connectionString || connectionString.includes("PLACEHOLDER")) {
        console.warn("[Observability] Connection string missing or default. Analytics restricted.");
        return;
    }

    // 3. Initialize SDK
    // Snippet in index.html initializes 'appInsights'
    if (window.appInsights) {
        if (typeof window.appInsights.loadAppInsights === 'function') {
            window.appInsights.loadAppInsights();
            console.log("[Observability] SDK Loaded via standard loader.");
        } else if (window.appInsights.initialize === true) {
            console.log("[Observability] SDK already initialized (Lite Loader).");
        } else {
            console.warn("[Observability] AppInsights SDK found but loader is missing or broken.");
        }
    }

    // 4. Custom Sanitization & Governance (Privacy PII Scrubbing)
    let privacyHits = 0;
    if (window.appInsights && typeof window.appInsights.addTelemetryInitializer === 'function') {
        window.appInsights.addTelemetryInitializer((envelope) => {
            let scrubbed = false;
            if (envelope.data && envelope.data.baseData) {
                const data = envelope.data.baseData;

                // Scrub PII from URL
                if (data.url) {
                    const originalUrl = data.url;
                    try {
                        const url = new URL(data.url);
                        data.url = url.origin + url.pathname;
                        if (originalUrl !== data.url) scrubbed = true;
                    } catch (e) {
                        data.url = "scrubbed-url";
                        scrubbed = true;
                    }
                }

                // Scrub Referrer
                if (data.referrerInfo && data.referrerInfo.referrer) {
                    const originalRef = data.referrerInfo.referrer;
                    try {
                        const ref = new URL(data.referrerInfo.referrer);
                        data.referrerInfo.referrer = ref.origin + ref.pathname;
                        if (originalRef !== data.referrerInfo.referrer) scrubbed = true;
                    } catch (e) {
                        data.referrerInfo.referrer = "external";
                        scrubbed = true;
                    }
                }
            }
            if (scrubbed) {
                privacyHits++;
                const hitElem = document.getElementById('privacy-hits');
                if (hitElem) hitElem.textContent = privacyHits;
            }
        });
    }

    // 5. Track High-Value Governance Events
    document.addEventListener('click', (e) => {
        // Track Resume Downloads
        const resumeBtn = e.target.closest('a[href*="Resume"], .btn-resume, [data-analytics="resume"]');
        if (resumeBtn) {
            window.appInsights && window.appInsights.trackEvent({
                name: 'ResumeDownload',
                properties: {
                    type: 'ExecutiveBrief',
                    url: resumeBtn.getAttribute('href')
                }
            });
            console.log("[Telemetry] Event: ResumeDownload");
        }

        // Track External Authority Links
        const extLink = e.target.closest('a[target="_blank"]');
        if (extLink && extLink.hostname !== window.location.hostname) {
            window.appInsights && window.appInsights.trackEvent({
                name: 'ExternalNavigation',
                properties: {
                    destination: extLink.href,
                    label: extLink.innerText.trim() || extLink.hostname
                }
            });
            console.log("[Telemetry] Event: ExternalNavigation -> " + extLink.hostname);
        }
    });

    // 6. System Health Heartbeat & UI Sync
    async function checkSystemHealth() {
        // Targets both Hero Widget and Potential Footer elements
        const statusVals = document.querySelectorAll('#status-val, #status-val-hero, .health-status-text');
        const statusDots = document.querySelectorAll('.status-dot, .health-indicator');
        const platformStatus = document.getElementById('platform-status');

        try {
            const isSubfolder = window.location.pathname.includes('/blog/') || window.location.pathname.includes('/pages/');
            const statusPath = isSubfolder ? '../status.json' : 'status.json';

            const start = performance.now();
            const response = await fetch(statusPath, { cache: 'no-store' });
            const end = performance.now();
            const latency = Math.round(end - start);

            if (response.ok) {
                const data = await response.json();

                statusVals.forEach(el => el.textContent = data.status || "Online");
                if (platformStatus) platformStatus.textContent = "Healthy";
                statusDots.forEach(dot => {
                    dot.style.background = "#10b981"; // Emerald-500
                    dot.classList.add('pulse');
                });

                // Update latency if element exists (matched with hero script)
                const latencyElem = document.getElementById('azure-latency');
                if (latencyElem) {
                    latencyElem.textContent = `${latency}ms`;
                    latencyElem.style.color = latency < 150 ? "#34d399" : "#fbbf24";
                }

                console.log(`[Observability] Health Check: ${data.status} (${latency}ms)`);
            } else {
                throw new Error("System Degraded");
            }
        } catch (e) {
            statusVals.forEach(el => el.textContent = "Offline");
            statusDots.forEach(dot => {
                dot.style.background = "#ef4444"; // Red-500
                dot.classList.remove('pulse');
            });
            console.error("[Observability] Health Check Failed:", e.message);
        }
    }

    // Initial check and periodic polling
    document.addEventListener('DOMContentLoaded', () => {
        checkSystemHealth();
        setInterval(checkSystemHealth, 30000); // 30s heartbeat

        // Sync UX Speed (Performance API)
        setTimeout(() => {
            const perf = window.performance.timing;
            if (perf) {
                const navTime = perf.loadEventEnd - perf.navigationStart;
                const speedElem = document.getElementById('ux-speed');
                if (speedElem && navTime > 0) {
                    speedElem.textContent = `${navTime}ms`;
                    speedElem.style.color = navTime < 1500 ? "#34d399" : "#fbbf24";
                }
            }
        }, 1000); // Wait for load event to finalize
    });

    console.log("[Observability] Governance Protocol Active.");
})();
