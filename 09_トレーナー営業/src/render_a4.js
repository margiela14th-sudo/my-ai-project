// 使い方: node src/render_a4.js <html> <pdf>  （A4横）
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.resolve(process.argv[2]));
await p.pdf({path:process.argv[3],width:'297mm',height:'210mm',printBackground:true});await b.close();})();
