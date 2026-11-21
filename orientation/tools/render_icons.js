// アイコン（Font Awesome 6 / react-icons）を SVG ファイルとして書き出すスクリプト
// 使い方: NODE_PATH=<react-icons を入れた node_modules> node render_icons.js <出力ディレクトリ>
// 生成済みの SVG は orientation/assets/icons/ にコミット済みなので、通常は再実行不要です。
const fs = require("fs");
const path = require("path");
const React = require("react");
const { renderToStaticMarkup } = require("react-dom/server");
const fa6 = require("react-icons/fa6");

const NAMES = [
  "FaChalkboardUser", "FaBook", "FaBookOpen", "FaPencil", "FaClipboardCheck",
  "FaCalendarCheck", "FaRotate", "FaHouse", "FaListCheck", "FaClock", "FaSun",
  "FaUtensils", "FaBroom", "FaPersonWalking", "FaSchool", "FaShirt", "FaBriefcase",
  "FaBuilding", "FaMobileScreen", "FaUserShield", "FaCamera", "FaCommentDots",
  "FaHandHoldingHeart", "FaFutbol", "FaMusic", "FaPeopleGroup", "FaPalette",
  "FaTrophy", "FaBus", "FaMasksTheater", "FaFlag", "FaLightbulb", "FaComments",
  "FaEarListen", "FaHandshake", "FaSeedling", "FaStar", "FaHeart", "FaQuestion",
  "FaMagnifyingGlass", "FaRoute", "FaPersonRunning", "FaMicrophone", "FaUsers",
  "FaKitMedical", "FaUserTie", "FaPhone", "FaBullhorn", "FaRecycle", "FaFaceSmile",
  "FaCircleCheck", "FaPenToSquare", "FaFlask", "FaHouseUser", "FaLock",
  "FaTriangleExclamation", "FaArrowsRotate", "FaMountainSun", "FaGamepad",
  "FaClipboardList", "FaCalculator", "FaGlobe", "FaRegFaceSmile", "FaBell",
  "FaDoorOpen", "FaHandsHolding", "FaUserGroup", "FaSquareCheck", "FaRegSquare",
];

const out = process.argv[2] || "icons";
fs.mkdirSync(out, { recursive: true });
let missing = [];
for (const n of NAMES) {
  const C = fa6[n];
  if (!C) { missing.push(n); continue; }
  const svg = renderToStaticMarkup(React.createElement(C, { size: 512, color: "#FFFFFF" }));
  const withNs = svg.includes("xmlns=") ? svg : svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"');
  fs.writeFileSync(path.join(out, n.replace(/^Fa/, "") + ".svg"), withNs);
}
console.log("written:", NAMES.length - missing.length, "missing:", missing.join(","));
