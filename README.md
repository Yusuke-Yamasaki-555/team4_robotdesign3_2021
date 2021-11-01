# Team4_RobotDesign3_2021
cit robot-design-3-2021 crane_x7

　このパッケージはROSとRvizを用いて、rt-net様より販売されているcrane_x7を制御するものです。
以下のコマンドを実行して、~/catkin_ws/src/ 上にこのパッケージをインストールしてください。

(ビルドする件)

このパッケージは、rt-net様のライセンスに則り、rt-net様が公開されているパッケージ ”crane_x7_ros” のインストールを前提としています。
　　crane_x7_ros：https://github.com/rt-net/crane_x7_ros

また、このパッケージに実装されているモーションは realsense-D435 を用いた画像処理を含んでいます。そのため、以下のパッケージを追加でインストールする必要があります。

　・rviz,gazeboにカメラのモデルと映像を適用(シュミレーション。実機関係なく)
　　Kuwamai様より
　　　https://github.com/Kuwamai/crane_x7_d435

　・（実機）
　　（多分#ntelのやつ）

実行する前に、crane_x7_d435/launch/bringup_sim.launch内でincludeされているlaunchファイルの参照先を、team4_robotdesign3_2021に書き換えてください。その後、以下のコマンドを実行してください。gazeboシュミレーションとRvizが立ち上がります。

業務連絡：
　各ディレクトリのREADME.mdは、好きに書き換えてくれて構わない。共有メモの感覚で。

中間発表スライド：
https://docs.google.com/presentation/d/10579iWYMIuUj-ryrvBYHtZIV1r_oiTxQpfvfWUjjHhE/edit?pli=1#slide=id.gfa179629e3_0_115