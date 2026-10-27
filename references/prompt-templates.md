# 超燃群像登场提示词模板

只使用用户实际需要的路径。所有输出规格变量只继承用户或上游明确值；未明确的值保持为空，不用建议值代填。

## 参考职责模板

```yaml
reference_roles:
  ref_01:
    role: identity_and_outfit
    characters: [C1, C2]
    preserve: [face, species, body_shape, outfit, weapon, primary_color]
  ref_02:
    role: scene_and_composition
    preserve: [relative_positions, depth_order, horizon]
  ref_03:
    role: material_and_detail
    characters: [C1]
    preserve: [surface_material, accessories, weapon_detail]
  ref_04:
    role: motion_or_lighting
    apply_only: [motion_rhythm, camera_path, light_direction]
```

没有足够证据时删除对应引用项，不虚构职责。样片原始信息缺失时，只使用 [style-guide.md](style-guide.md) 中已经转写的创作规则，不声称引用了具体样片。

## 身份锁模板

```yaml
identity_lock:
  character_id: {C1}
  source_references: [{ref_01}, {ref_03}]
  permanent_design:
    face_or_head: {可见特征}
    species: {物种或人类}
    body_shape: {体型与比例}
    hair: {发型或毛发}
    outfit: {服装轮廓与材质}
    accessories: {饰品}
    weapon: {原有武器与持握手}
    primary_color: {定性色彩关系}
    energy_signature: {专属能量形态与综合色倾向}
  animatable_elements: [{头发}, {披风}, {飘带}, {羽毛}, {尘土}, {能量}]
  unknowns: [{无法从参考确认的维度}]
```

## 一键模式完整生成指令

```text
根据上传参考生成一段高能群像登场视频。

参考职责：
{reference_roles}

身份与人数：
{identity_lock_summary}
保持去重后的 {character_count} 名角色一一对应；单人段只出现当前角色，最终集结每名角色恰好出现一次。

必须保留：
{preserve}

允许改变：
只改变动作、技能表现、镜头、环境动态、粒子、转场与声音；冻结用户没有要求改变的身份、原始画风、剧情事实、构图和关键道具。

统一世界锚点：
环境：{environment_anchor}
主光方向：{light_anchor}
风或气流方向：{wind_anchor}
地平线与空间方向：{spatial_anchor}
基础粒子：{particle_anchor}

整数秒时间轴：
{timeline_from_script}

逐角色编排：
{character_segments}

全员集结：
{group_formation_segment}

声音：
{music_direction}
{sound_layers}
每个主音效对应一个清楚画面事件，技能峰值与动作峰值同步。

连续性：
{continuity_lock}

输出规格：
{only_explicit_output_spec}

负面约束：
{negative_constraints}
```

## 逐角色镜头模板

为 `C1…Cn` 逐一填写。相邻角色至少改变入场向量、镜头运动、技能表现、转场方式和环境粒子中的三项。

```text
角色：{character_id}
参考职责：{identity_reference} 负责身份与服装；{detail_reference} 负责武器或材质；{group_reference} 负责关系与站位。

起始状态：
{角色初始位置、朝向、重心、武器状态、环境、主光和风向}

主体动作：
{入场或显形} → {蓄势} → {突然加速} → {招牌动作或技能命中} → {顿挫} → {余势收招与身份确认}
力量从脚底或身体重心传到躯干、肩胯、肢体，再传到武器或技能；禁止只有局部摆动。

环境响应：
{地面、碎屑、烟尘、衣发、披风、粒子、技能补光和冲击波的因果反馈}

镜头运动：
景别：{shot_size}
机位：{camera_height_and_angle}
主向量：{camera_vector}
路径与速度：{camera_path_and_speed_curve}
命中响应：{impact_response}
结束构图：{ending_composition}

风格保持：
保持 {original_medium}、{shape_language}、{material_language}、{rendering_language} 与 {color_relationship}；不强制改成写实 CG。

结束状态：
{角色位置、姿态、武器方向、能量衰减、环境状态和镜头稳定状态}

连续性继承：
下一镜头继承 {identity_anchor}、{prop_anchor}、{scene_anchor}、{light_anchor}、{wind_anchor}、{spatial_anchor} 和 {transition_anchor}。

输出规格：
{only_explicit_output_spec}
```

## 角色类型模块

从对应类型选择一组，不叠加两套完整技能：

```yaml
motion_module:
  heavy:
    entrance: [高处砸落, 正面冲锋, 烟尘中起身]
    impact: [盾击, 重锤落地, 地裂, 范围冲击]
    camera: [超低机位后拉, 短促方向震动, 冲击后仰拍稳定]
    sound: [重脚步, 金属负重, 低频撞击, 碎石]
  blade:
    entrance: [拔刃显形, 侧向踏入, 背光转身]
    impact: [横斩, 突刺, 回旋, 格挡反击]
    camera: [贴刃跟拍, 侧向平移, 刃锋掠镜后切近景]
    sound: [出鞘, 金属切风, 命中, 余振]
  agile:
    entrance: [高速掠入, 翻越前景, 阴影闪现]
    impact: [连续短斩, 瞬移, 残影, 背身收招]
    camera: [甩镜追踪, 近身掠过, 单次受控荷兰角]
    sound: [快速whoosh, 短促金属, 低声瞬移]
  firearm:
    entrance: [掩体起身, 滑入, 机械展开]
    impact: [瞄准, 装填, 开火, 后坐力, 能量炮]
    camera: [枪口超特写, 肩后跟拍, 短暂弹道追踪]
    sound: [机械咔哒, 蓄能, 枪炮, 弹壳]
  projectile:
    entrance: [跃入高点, 侧身旋转, 落地搭箭]
    impact: [拉弓, 蓄能箭, 散射, 箭矢追踪]
    camera: [受控环绕拉弓, 眼弦箭头特写, 随箭前冲]
    sound: [弓弦张力, 箭鸣, 穿空, 命中]
  magic:
    entrance: [漂浮落下, 法阵显形, 披风揭示]
    impact: [法球, 符文, 护盾, 召唤, 元素爆发]
    camera: [慢弧绕行后突然推近, 峰值时稳住面部]
    sound: [低频蓄能, 符文层, 能量释放, 晶体]
  creature:
    entrance: [远处奔来, 破土, 俯冲, 四足爬出]
    impact: [扑咬, 吼叫, 爪击, 尾扫, 元素吐息]
    camera: [贴地后退, 广角近身, 咆哮面部特写]
    sound: [呼吸, 爪地, 吼叫, 撞击, 碎屑]
  mech:
    entrance: [系统启动, 舱门开启, 部件组装]
    impact: [武器展开, 喷射, 扫描, 导弹, 光束]
    camera: [机械细节超特写后拉全身, 沿喷射方向跟随]
    sound: [伺服, 锁定, 启动音, 喷射, 能量束]
  unarmed:
    entrance: [风中定步, 翻滚, 拳掌起势]
    impact: [拳脚组合, 掌风, 气场, 环境操控]
    camera: [肢体方向跟拍, 命中短震, 近景确认]
    sound: [衣料, 拳风, 脚步, 身体冲击]
```

## 转场模板

```text
前一镜头结束状态：{previous_end_state}
转场触发：{武器或披风擦屏 | 技能爆闪 | 弹道或能量轨迹 | 烟尘雨雪碎石填屏 | 动作匹配 | 甩镜}
空间连续性：保持 {movement_direction}、{light_direction}、{wind_direction} 和 {horizon}。
下一镜头起始状态：{next_start_state}
转场短促完成；继承帧率后才把转场时长换算为整数帧。
```

## 全员集结模板

该段必须作为完整高潮保留。只取消自动片尾文字标题，不得删除集结进入、阵型建立、角色落位、微动定格、镜头稳定和声音收束。

```text
起始状态：
最后一名单人角色完成技能命中、顿挫和余势；其动作方向、能量轨迹、烟尘或前景遮挡成为集结转场的直接触发，环境、主光、风向和基础粒子连续。

集结进入：
使用 {冲击闪光 | 全员落地 | 前景遮挡揭示 | 高速拉远进入宽景}，在音乐重拍上显示全部角色；同步一次 {低频落地 | 全频冲击 | 环境爆发}，并让地面、碎屑、衣摆、武器和能量共同响应。

阵型规则：
- 群像参考存在时，恢复原图人物数量、左右关系、前后层级、主次比例和站位逻辑。
- 群像参考没有明确站位时，使用“主角居中或略前、重型角色后排支撑、轻型角色前侧、远程角色两翼”，再按轮廓和武器方向调整。
- 只有单人参考时，根据领导感、体型、轮廓高度和武器展开方向建立中心与两翼；无主角时以第一张参考中的角色为视觉中心。
- 偶数人数使用中轴双核心或中央留缝；角色前后错落，保留清楚轮廓间隙，头部和武器互不遮挡。

落位动作：
全员在最终段前半程完成 {最后半步 | 落地 | 转身 | 抬头 | 武器归位}，明确表现从运动状态进入阵型的过程；禁止直接把原图作为无过渡静帧贴回。

微动定格：
角色落位后，错开呼吸、眨眼和重心变化；统一风向继续作用于头发、披风、耳朵、尾巴、羽毛与粒子；武器和能量保留余振、热气、火花或光衰减。

镜头：
集结瞬间承接动作冲击，随后迅速稳定为英雄式宽景；允许非常轻微的前推或漂移，不持续抖动，不继续高速甩镜。

声音收束：
集结冲击与音乐重拍同步，随后保留环境声、武器余振和混响尾；移除自动片尾文字标题时，仍完整保留该声音高潮与收束。

结束状态：
所有角色恰好出现一次，身份清晰，阵型完整，空间、光源、风向、地平线和角色比例连续，群像保持自然微动。

输出规格：
{only_explicit_output_spec}
```

## 声音模板

```text
配乐方向：{用户或上游明确方向；未明确时只描述能量曲线，不指定固定曲风}
前段：低频脉冲、环境底与稀疏打击建立期待。
中段：每名角色的主动作增加一层节奏或配器，动作峰值与重拍同步。
后段：全员集结达到高潮，以尾音、重击或短收束结束。
音效层：
1. 环境底：{风、雨雪、尘土、空间氛围}
2. 身体与服装：{脚步、落地、布料、毛发、护甲}
3. 武器机械：{拔出、装填、挥动、弓弦、锁定}
4. 技能：{蓄能、释放、飞行、命中、衰减}
5. 强调层：{whoosh、riser、sub hit、冲击尾}
每个大音效只服务一个明确画面事件，不持续堆满所有频段。
```

## 连续性块

```yaml
continuity_lock:
  character_anchor: {人数、身份、脸部、体型、服装、主色}
  prop_anchor: {武器类型、持握手、饰品、关键道具}
  scene_anchor: {环境、地面材质、背景标志物、地平线}
  material_anchor: {原始媒介、角色与场景材质}
  light_anchor: {主光方向、明暗关系、技能补光回落状态}
  camera_anchor: {运动轴、角色出入画方向、结束构图}
  motion_anchor: {动作结束姿态、速度状态、余势}
  environment_anchor: {风向、基础粒子、天气、气流}
```

## 负面提示词模板

```text
禁止换脸、改变物种、发型、服装、武器或主色；禁止复制、融合、互换、遗漏或新增角色；禁止把同一角色的不同视角识别为多人；禁止只堆特效而没有身体传力；禁止动作全程匀速、漂浮或软绵；禁止全程手持抖动、连续整圈环绕、无意义鱼眼和重复运镜；禁止镜头穿模、武器穿身、多余肢体、漂浮道具、断裂衣物和错误握持；禁止技能持续遮挡身份识别点；禁止最终群像完全静止；禁止改变原始二维、三维、写实、卡通、像素、定格或其他美术语言；禁止填写未由用户或上游明确给出的输出规格；禁止新增未经明确要求的屏幕文本元素。
```
