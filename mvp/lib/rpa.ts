import type { Occurrence } from './data';
export type RpaBatch = {execucao:string;atualizado:string;alertas:Pick<Occurrence,'id'|'category'|'status'|'lat'|'lng'>[]};
export function parseRpa(text:string):RpaBatch {
 const data=JSON.parse(text.replace(/^\uFEFF/,''));
 if(!data||typeof data.execucao!=='string'||!data.execucao.trim()||typeof data.atualizado!=='string'||!Number.isFinite(Date.parse(data.atualizado))||!Array.isArray(data.alertas))throw Error('Arquivo inválido. Importe alertas_ativos.json gerado pelo robô.');
 if(data.alertas.length>10000)throw Error('O limite desta demonstração é de 10.000 alertas.');
 const ids=new Set<string>();
 const alertas=data.alertas.map((a:any)=>{
  if(!a||typeof a.id!=='string'||!a.id.trim()||ids.has(a.id)||typeof a.category!=='string'||!a.category.trim()||!['Registrada','Em análise'].includes(a.status)||typeof a.lat!=='number'||!Number.isFinite(a.lat)||Math.abs(a.lat)>90||typeof a.lng!=='number'||!Number.isFinite(a.lng)||Math.abs(a.lng)>180)throw Error('Alerta inválido ou ID repetido. A importação anterior foi preservada.');
  ids.add(a.id);return {id:a.id,category:a.category,status:a.status,lat:a.lat,lng:a.lng};
 });
 return {execucao:data.execucao,atualizado:data.atualizado,alertas};
}
export function rpaRows(batch:RpaBatch):Occurrence[]{
 return batch.alertas.map(a=>({...a,title:`Alerta RPA · ${a.category}`,address:`${a.lat.toFixed(5)}, ${a.lng.toFixed(5)}`,description:'Resultado da triagem importado neste navegador. Retrato do lote na data indicada; não altera o cadastro original.',created:batch.atualizado,updated:batch.atualizado,photo:null,demo:0}));
}

// Os cadastros atuais prevalecem sobre um retrato importado do mesmo ID.
export function mergeMapAlerts(rows:Occurrence[], imported:Occurrence[]):Occurrence[]{
 const merged=new Map(imported.map(row=>[row.id,row]));
 for(const row of rows)merged.set(row.id,row);
 return [...merged.values()].filter(row=>row.status!=='Resolvida');
}
