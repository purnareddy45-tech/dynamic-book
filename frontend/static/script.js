// ===============================
// BACKEND URL
// ===============================

// 🔹 LOCAL BACKEND (FastAPI running locally)
// IMPORTANT: backend runs on PORT 10000
const API_URL = "http://127.0.0.1:10000/process-file/";

// 🔹 PRODUCTION (Render)
// const API_URL = "https://dynamic-book.onrender.com/process-file/";

// ===============================
// STATUS HANDLER
// ===============================
function setStatus(text, isError = false) {
  const s = document.getElementById("status");
  s.textContent = text;
  s.className = isError ? "status-error" : "";
}

// ===============================
// CLEAR OUTPUT
// ===============================
function clearOutput() {
  document.getElementById("summary").textContent = "";
  document.getElementById("notes").textContent = "";
  document.getElementById("flashcards").textContent = "";
  document.getElementById("questions").textContent = "";
  setStatus("Ready");
  document.getElementById("fileInput").value = "";
}

// ===============================
// FILE UPLOAD
// ===============================
async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a PDF or DOCX file first.");
    return;
  }

  clearOutput();
  setStatus("Uploading and processing...");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const resp = await fetch(API_URL, {
      method: "POST",
      body: formData
    });

    if (!resp.ok) {
      setStatus(`Server error (${resp.status})`, true);
      return;
    }

    const data = await resp.json();

    // ===============================
    // SUMMARY & NOTES
    // ===============================
    document.getElementById("summary").textContent =
      data.summary || "No summary returned.";

    document.getElementById("notes").textContent =
      data.notes || "No notes returned.";

    // ===============================
    // FLASHCARDS
    // ===============================
    const flashcards = data.flashcards || [];
    if (Array.isArray(flashcards) && flashcards.length > 0) {
      let fcText = "";
      flashcards.forEach((c, i) => {
        fcText += `Flashcard ${i + 1}:\n`;
        fcText += `Q: ${c.front}\n`;
        fcText += `A: ${c.back}\n\n`;
      });
      document.getElementById("flashcards").textContent = fcText;
    } else {
      document.getElementById("flashcards").textContent =
        "No flashcards generated.";
    }

    // ===============================
    // QUESTIONS
    // ===============================
    const questions = data.questions || {};
    let qText = "";

    if (questions.mcqs?.length) {
      qText += "MCQs:\n";
      questions.mcqs.forEach((m, i) => {
        qText += `${i + 1}. ${m.question}\n`;
        m.options?.forEach((opt, j) => {
          qText += `   ${String.fromCharCode(65 + j)}. ${opt}\n`;
        });
        qText += `   Answer: ${m.answer}\n\n`;
      });
    }

    if (questions.short_questions?.length) {
      qText += "\nShort Questions:\n";
      questions.short_questions.forEach((s, i) => {
        qText += `${i + 1}. ${s}\n`;
      });
    }

    if (questions.long_questions?.length) {
      qText += "\nLong Questions:\n";
      questions.long_questions.forEach((l, i) => {
        qText += `${i + 1}. ${l}\n`;
      });
    }

    document.getElementById("questions").textContent =
      qText || "No questions generated.";

    setStatus("Done ✅");

  } catch (err) {
    console.error(err);
    setStatus("Failed to connect to backend ❌", true);
  }
}
