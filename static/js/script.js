async function generatePlan() {
  const goal = document.getElementById("userGoal").value;
  const resultDiv = document.getElementById("result");
  const loading = document.getElementById("loading");
  const stepsList = document.getElementById("resSteps");

  if (!goal) return alert("Enter a project goal first!");

  loading.classList.remove("hidden");
  resultDiv.classList.add("hidden");
  stepsList.innerHTML = "";

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal: goal }),
    });

    const data = await response.json();
    if (data.error) throw new Error(data.error);

    // UI Updates
    document.getElementById("resTitle").innerText = data.project_name;
    document.getElementById("resDiff").innerText =
      `${data.difficulty_level} • ~${data.estimated_hours || 0} hrs`;

    data.steps.forEach((step) => {
      const li = document.createElement("li");
      li.className =
        "bg-slate-700/40 p-5 rounded-xl border border-slate-600 hover:border-blue-500 transition-all group";
      li.innerHTML = `
                <div class="flex justify-between items-start mb-2">
                    <h3 class="font-bold text-blue-300">${step.milestone}</h3>
                    <span class="text-xs font-mono bg-slate-900 px-2 py-1 rounded text-emerald-400 border border-emerald-500/30">${step.tech_stack}</span>
                </div>
                <p class="text-sm text-slate-300 leading-relaxed">${step.description}</p>
            `;
      stepsList.appendChild(li);
    });

    resultDiv.classList.remove("hidden");
  } catch (err) {
    console.error(err);
    alert("Architect Error: " + err.message);
  } finally {
    loading.classList.add("hidden");
  }
}
