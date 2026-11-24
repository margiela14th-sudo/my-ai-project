import { marked } from "/vendor/marked.js";

const $ = (s) => document.querySelector(s);
const form = $("#lessonForm");
const result = $("#result");
const status = $("#status");
let options;
let markdown = "";
let controller = null;

const MAX_GRADE = { elementary: 6, juniorHigh: 3 };

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

// 生成された本文中の生のHTMLは実行させず、文字として表示する
marked.use({ renderer: { html: ({ text }) => escapeHtml(text) } });

function render() {
  result.innerHTML = marked.parse(markdown);
}

function fillGrades() {
  const level = form.schoolLevel.value;
  const prev = form.grade.value;
  form.grade.innerHTML = "";
  for (let g = 1; g <= MAX_GRADE[level]; g++) form.grade.add(new Option(`${g}年`, String(g)));
  if (prev && Number(prev) <= MAX_GRADE[level]) form.grade.value = prev;
}

function fillSubjects() {
  const level = form.schoolLevel.value;
  const grade = Number(form.grade.value);
  const regular = form.classSetting.value === "regular";
  const prev = form.subject.value || "math";
  form.subject.innerHTML = "";
  for (const s of options.subjects) {
    // 特別支援学級・学校・通級は教育課程を独自に編成できるため全教科を出す
    if (regular && !s.grades[level].includes(grade)) continue;
    form.subject.add(new Option(s.name, s.id));
  }
  if ([...form.subject.options].some((o) => o.value === prev)) form.subject.value = prev;
}

function toggleSpecial() {
  $("#specialBox").hidden = form.classSetting.value === "regular";
}

async function init() {
  options = await (await fetch("/api/options")).json();

  for (const [v, label] of Object.entries(options.classSettings)) form.classSetting.add(new Option(label, v));
  $("#disabilityList").innerHTML = Object.entries(options.disabilityTypes)
    .map(([v, l]) => `<label class="check"><input type="checkbox" name="disabilityTypes" value="${v}" />${l}</label>`)
    .join("");
  $("#planTypes").innerHTML = options.planTypes
    .map(
      (p, i) => `<label class="card"><input type="radio" name="planType" value="${p.type}" ${i === 0 ? "checked" : ""} />
        <strong>${p.label}</strong><span>${p.purpose}</span></label>`,
    )
    .join("");

  fillGrades();
  fillSubjects();
  toggleSpecial();
  form.schoolLevel.addEventListener("change", () => { fillGrades(); fillSubjects(); });
  form.grade.addEventListener("change", fillSubjects);
  form.classSetting.addEventListener("change", () => { toggleSpecial(); fillSubjects(); });

  const s = await (await fetch("/api/settings")).json();
  if (!s.hasApiKey) openSettings();
}

function collect() {
  const fd = new FormData(form);
  const num = (k) => (fd.get(k) ? Number(fd.get(k)) : undefined);
  const str = (k) => (fd.get(k) || "").toString().trim() || undefined;
  return {
    schoolLevel: fd.get("schoolLevel"),
    grade: Number(fd.get("grade")),
    subject: fd.get("subject"),
    planType: fd.get("planType"),
    unitName: str("unitName") ?? "",
    lessonNumber: num("lessonNumber"),
    totalLessons: num("totalLessons"),
    minutes: num("minutes"),
    classSetting: fd.get("classSetting"),
    disabilityTypes: form.classSetting.value === "regular" ? [] : fd.getAll("disabilityTypes"),
    intellectualStage: form.classSetting.value === "regular" ? undefined : str("intellectualStage"),
    lessonFocus: str("lessonFocus"),
    studentProfile: str("studentProfile"),
    supportNotes: str("supportNotes"),
    textbook: str("textbook"),
    researchTheme: str("researchTheme"),
    extraRequests: str("extraRequests"),
  };
}

function setBusy(busy) {
  $("#generateBtn").disabled = busy;
  $("#stopBtn").hidden = !busy;
  for (const id of ["#copyBtn", "#downloadBtn", "#printBtn"]) $(id).disabled = busy || !markdown;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const err = $("#formError");
  err.hidden = true;
  const body = collect();
  if (!body.unitName) {
    err.textContent = "単元名を入力してください。";
    err.hidden = false;
    form.unitName.focus();
    return;
  }

  markdown = "";
  render();
  controller = new AbortController();
  setBusy(true);
  status.textContent = "副担任が構想を練っています…（1〜3分ほどかかります）";

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    if (!res.ok) {
      const j = await res.json().catch(() => ({}));
      throw new Error(j.error || "生成に失敗しました。");
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    status.textContent = "書いています…";
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      markdown += decoder.decode(value, { stream: true });
      render();
    }
    status.textContent = "できあがりました。内容を確認して、必要なところを直してお使いください。";
  } catch (e2) {
    if (e2.name === "AbortError") status.textContent = "止めました。";
    else {
      status.textContent = "";
      err.textContent = e2.message;
      err.hidden = false;
    }
  } finally {
    controller = null;
    setBusy(false);
  }
});

$("#stopBtn").addEventListener("click", () => controller?.abort());

$("#copyBtn").addEventListener("click", async () => {
  await navigator.clipboard.writeText(markdown);
  status.textContent = "コピーしました。";
});

$("#downloadBtn").addEventListener("click", () => {
  const b = collect();
  const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `指導案_${b.unitName || "無題"}.md`;
  a.click();
  URL.revokeObjectURL(a.href);
});

$("#printBtn").addEventListener("click", () => window.print());

// ---- 設定 ----
const dialog = $("#settings");
async function openSettings() {
  const s = await (await fetch("/api/settings")).json();
  $("#keyState").textContent = s.hasApiKey ? "APIキーは登録済みです（変更する場合のみ入力）。" : "APIキーが未登録です。";
  $("#settingsError").hidden = true;
  dialog.showModal();
}
$("#openSettings").addEventListener("click", openSettings);
$("#closeSettings").addEventListener("click", () => dialog.close());
$("#settingsForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const apiKey = e.target.apiKey.value.trim();
  const res = await fetch("/api/settings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ apiKey }),
  });
  if (!res.ok) {
    const j = await res.json().catch(() => ({}));
    $("#settingsError").textContent = j.error || "保存できませんでした。";
    $("#settingsError").hidden = false;
    return;
  }
  e.target.apiKey.value = "";
  dialog.close();
  status.textContent = "APIキーを保存しました。";
});

init();
