<!--
 * @Author: Innis
 * @Description: 
 * @Date: 2022-03-31 07:45:41
 * @LastEditTime: 2022-03-31 07:45:42
 * @FilePath: \0328P-rete\keyWords.md
-->

一条产生式规则包括左、右两部分

left hand side(RHS):左部包含若干个正或负模式（ pattern）,condation

right hand side(RHS): action/a

识别网络中包括了两类节点：单输入结点（ one－input node） 负责测试事实是否能够匹配一个模式，成功通过测试的标牌被存到α存储器。双输入结点()（ two－input node） 负责测试两个匹配于不同模式的标牌是否满足变量的一致性约束，通过测试的两个标牌被合成一个并被存到β存储器。如果有事实遍历完整个网络结构，就到达了终结结点（ terminal node） ，这时冲突集（ conflict set） 就发生相应的改变。
