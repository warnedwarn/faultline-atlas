'use client';
import {createAccount,createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
export const CONTRACT=(process.env.NEXT_PUBLIC_CONTRACT_ADDRESS||'0x95c8D011dE4C6ccB33fD7e575B0D5385AcB3eC14') as `0x${string}`;
export const EXPLORER=process.env.NEXT_PUBLIC_EXPLORER_BASE_URL||'https://explorer-studio.genlayer.com';
const endpoint='https://studio.genlayer.com/api';
const reader:any=createClient({chain:studionet,endpoint,account:createAccount()});
let wallet:any;
export async function connect(){const p:any=(window as any).ethereum;if(!p)throw Error('A browser wallet is required');const[a]=await p.request({method:'eth_requestAccounts'});if((await p.request({method:'eth_chainId'})).toLowerCase()!=='0xf22f')await p.request({method:'wallet_switchEthereumChain',params:[{chainId:'0xf22f'}]});wallet=createClient({chain:studionet,endpoint,account:a,provider:p});return a}
export function read(name:string,args:any[]=[]){if(!CONTRACT)throw Error('Contract deployment is not configured');return reader.readContract({address:CONTRACT,functionName:name,args})}
export async function write(name:string,args:any[]=[]){if(!wallet)throw Error('Connect a wallet before dispatching');const hash=await wallet.writeContract({address:CONTRACT,functionName:name,args,value:0n});await wallet.waitForTransactionReceipt({hash,status:'ACCEPTED',retries:120,interval:5000});return hash as string}
