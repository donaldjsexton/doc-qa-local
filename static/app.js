const $ = (s) => document.querySelector(s);

$("#uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = $("#file").files[0];
  if (!f) return;
  const fd = new FormData();
  fd.append("file", f);
  const docId = $("#docId").value.trim();
  if (docId) fd.append("doc_id", docId);

  $("#ingestOut").textContent = "Uploading...";
  const res = await fetch("/api/upload", { method: "POST", body: fd });
  const data = await res.json();
  $("#ingestOut").textContent = JSON.stringify(data, null, 2);
});

$("#askForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = $("#question").value.trim();
  const doc_id = $("#askDocId").value.trim();
  if (!question) return;

  $("#answer").textContent = "Thinking...";
  $("#sources").textContent = "";

  const res = await fetch("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, doc_id: doc_id || null })
  });
  const data = await res.json();
  $("#answer").textContent = data.answer || "(no answer)";
  if (data.sources && data.sources.length) {
    const lines = data.sources.map((s, i) =>
      `#${i+1}  score=${(s.score ?? 0).toFixed(4)}  doc_id=${s.doc_id}  chunk=${s.chunk}\n${(s.text||'').slice(0, 300)}`
    );
    $("#sources").textContent = lines.join("\n\n");
  }
});

