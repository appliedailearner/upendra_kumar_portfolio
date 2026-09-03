# How to Test the BlogMaker V2 "Vice President" Update

This guide outlines exactly how to test the new `master prompts\blogmaker.md` file to verify that the AI successfully adopts the **Cloud Practice Director / VP** persona and outputs high-level strategic content alongside your technical architecture.

---

## 1. The Setup

Open your preferred AI tool (ChatGPT, Claude, etc.) and start a fresh, new conversation. You must do this so the AI doesn't carry over any previous context.

## 2. Feed the Engine

Copy and paste the entire contents of your newly updated `c:\MyResumePortfolio\master prompts\blogmaker.md` file into the chat box.

Directly underneath the pasted prompt, add your raw testing notes. Use the example provided below:

***[PASTE THE ENTIRE BLOGMAKER.MD CONTENT HERE]***

Then, add this exact text below it:

> **My Raw Notes for the New Post:**
> "I want to write about Azure Landing Zones. Last week, I looked at a client's environment. They had 40 different subscriptions with no centralized firewalls or ExpressRoute connectivity. Every team was just deploying their own disjointed VNETs. They had a huge security risk because developers were just assigning Public IPs to VMs directly to access the internet. Also, their monthly Azure bill was $60k higher than it should be because they had duplicate VPN gateways everywhere instead of a single Hub. I told them to use a Hub and Spoke topology, enforce Azure Policies to block Public IPs, and route all traffic through a centralized Azure Firewall in the Hub."

## 3. Hit Enter/Send

Allow the AI to process the prompt and your raw notes.

---

## 4. What to Look For (The Success Criteria)

If the V2 update is working correctly, you should actively observe the AI do the following things in its output:

### ✅ Criteria 1: The Executive Impact Summary (The VP Check)
At the very top of the generated text (or embedded in the HTML), you should see a clear breakdown of the **Business Problem**, the **Strategic Play**, and the **Executive ROI**. 
*   *Instead of:* "Here's how to build a Hub and Spoke."
*   *It should say:* "The organization was hemorrhaging $720k annually due to infrastructure sprawl and faced critical exfiltration risks. Implementing a centralized Landing Zone consolidated connectivity, resulting in immediate ROI."

### ✅ Criteria 2: Tone and Jargon Shift
The AI should fundamentally shift the tone from a "Network Engineer" to a "Practice Director."
*   *Instead of:* "We deleted their VPN gateways and added an Azure Firewall."
*   *It should say:* "We eliminated shadow IT by enforcing a centralized Hub-and-Spoke operating model, mitigating public exposure via Azure Policy guardrails."

### ✅ Criteria 3: The New HTML Components (The Boilerplate Check)
When the AI generates the massive HTML code block in Phase 2, look at the bottom of the HTML output before the `</body>` tag. 
*   You should see the embedded JSON dictionary (`const glossaryTerms = { ... }`).
*   You should see the Javascript for the `.eli5-term` Tooltips, the Checklist `localStorage` engine, and the Table of Contents `IntersectionObserver`.

## 5. Review the Output

If the output meets these criteria, your V2 BlogMaker prompt is successfully tuned for the 60-90 LPA leadership level. You can now use this exact prompt structure with any of your raw thoughts to generate elite, C-suite ready architectural content.
