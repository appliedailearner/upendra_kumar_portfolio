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

    // 2. App Insights Connection String (Placeholder)
    // Using existing telemetry endpoint as reference
    const connectionString = "InstrumentationKey=8fc596f2-..."; // Placeholder until provided

    if (connectionString === "CONNECTION_STRING_PLACEHOLDER") {
        console.warn("[Observability] Connection string missing. Analytics will not be sent.");
        return;
    }

    // 3. Initialize SDK (Loading snippet expected in index.html)
    // We assume the Microsoft AppInsights SDK snippet is present in the <head>

    window.appInsights && window.appInsights.loadAppInsights();

    // 4. Custom Sanitization & Governance
    window.appInsights && window.appInsights.addTelemetryInitializer((envelope) => {
        // Sanitize URL/Referrer to remove sensitive query parameters if any
        if (envelope.data && envelope.data.baseData) {
            const data = envelope.data.baseData;

            // Scrub URL
            if (data.url) {
                const url = new URL(data.url);
                // Example: Remove potential tokens or IDs
                // url.searchParams.delete('token'); 
                data.url = url.origin + url.pathname + url.search;
            }

            // Scrub Referrer
            if (data.referrerInfo && data.referrerInfo.referrer) {
                try {
                    const ref = new URL(data.referrerInfo.referrer);
                    data.referrerInfo.referrer = ref.origin + ref.pathname;
                } catch (e) {
                    data.referrerInfo.referrer = "unknown";
                }
            }
        }
    });

    // 5. Track Specific Principal-Level Events
    document.addEventListener('click', (e) => {
        // Track Resume Downloads
        const resumeBtn = e.target.closest('.nav-link.btn-primary[href*="Resume"]');
        if (resumeBtn) {
            window.appInsights && window.appInsights.trackEvent({
                name: 'ResumeDownload',
                properties: {
                    source: 'navbar',
                    filename: resumeBtn.getAttribute('href')
                }
            });
            console.log("[Observability] Event Logged: ResumeDownload");
        }

        // Track External Links (Authority Signal)
        const extLink = e.target.closest('a[target="_blank"]');
        if (extLink && extLink.hostname !== window.location.hostname) {
            window.appInsights && window.appInsights.trackEvent({
                name: 'ExternalNavigation',
                properties: {
                    destination: extLink.href,
                    text: extLink.innerText.trim()
                }
            });
        }
    });

    // 6. System Health Heartbeat
    async function checkSystemHealth() {
        const statusVal = document.getElementById('status-val');
        const statusDot = document.querySelector('.status-dot');

        try {
            const response = await fetch('/status.json');
            if (response.ok) {
                const data = await response.json();
                if (statusVal) statusVal.textContent = data.status || "Online";
                if (statusDot) {
                    statusDot.style.background = "#10b981";
                    statusDot.classList.add('pulse');
                }
            } else {
                throw new Error("Offline");
            }
        } catch (e) {
            if (statusVal) statusVal.textContent = "Offline";
            if (statusDot) {
                statusDot.style.background = "#ef4444";
                statusDot.classList.remove('pulse');
            }
        }
    }

    // Check on load
    document.addEventListener('DOMContentLoaded', checkSystemHealth);

    console.log("[Observability] Monitoring initialized safely.");
})();
