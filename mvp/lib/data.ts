export type Occurrence={id:string;title:string;category:string;address:string;description:string;lat:number;lng:number;status:string;created:string;updated:string;photo:string|null;demo:number};
export const categories=['Buraco','Entulho','Obstáculo','Rampa obstruída'];
export const statuses=['Registrada','Em análise','Resolvida'];
export const seeds:Occurrence[]=[
 {id:'fiap-demo-1',title:'Passagem bloqueada por entulho',category:'Entulho',address:'Entorno da FIAP · ponto fictício A',description:'Exemplo fictício: materiais ocupando a faixa de passagem de pedestres.',lat:-23.5737,lng:-46.6231,status:'Registrada'},
 {id:'fiap-demo-2',title:'Desnível na calçada',category:'Buraco',address:'Av. Lins de Vasconcelos · ponto fictício B',description:'Exemplo fictício: desnível que dificulta a passagem de uma cadeira de rodas.',lat:-23.5745,lng:-46.6228,status:'Em análise'},
 {id:'fiap-demo-3',title:'Acesso à rampa liberado',category:'Rampa obstruída',address:'Entorno da FIAP · ponto fictício C',description:'Exemplo fictício de ocorrência resolvida após desobstrução da passagem.',lat:-23.5733,lng:-46.6241,status:'Resolvida'},
 {id:'fiap-demo-4',title:'Objeto na faixa de circulação',category:'Obstáculo',address:'Entorno da FIAP · ponto fictício D',description:'Exemplo fictício: objeto ocupando parte da calçada.',lat:-23.5748,lng:-46.6240,status:'Registrada'}
].map(x=>({...x,created:'2026-11-07T12:00:00Z',updated:'2026-11-07T15:00:00Z',photo:null,demo:1}));

// Referência: mapa vinculado pela página oficial de contato da FIAP.
export const campus={lat:-23.5740619,lng:-46.6231674,name:"FIAP · Campus Aclimação",address:"Av. Lins de Vasconcelos, 1222 e 1264"};
