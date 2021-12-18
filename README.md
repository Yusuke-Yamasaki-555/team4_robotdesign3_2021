# Team4_RobotDesign3_2021
cit robot-design-3-2021 crane_x7
---
# このパッケージについて

このパッケージは、rt-net様より販売されているcrane_x7を制御するものです。オリジナルのパッケージは[こちら](https://github.com/rt-net/crane_x7_ros)です。
---
# 実行環境
- ROS Noetic
- Ubuntu 20.04.3 LTS
- ROS Distribution: Noetic Ninjemys 1.15.7
- Rviz 
- Gazebo 
- MoveIt

#　セットアップ
1. 
以下のコマンドを実行して、~/catkin_ws/src/ 上にこのパッケージをインストールしてください。

(ビルドする件)

このパッケージは、rt-net様のライセンスに則り、rt-net様が公開されているパッケージ ”crane_x7_ros” のインストールを前提としています。
　　crane_x7_ros：https://github.com/rt-net/crane_x7_ros

また、このパッケージに実装されているモーションは realsense-D435 を用いた画像処理を含んでいます。そのため、以下のパッケージを追加でインストールする必要があります。

　・rviz,gazeboにカメラのモデルと映像を適用(シミュレーション。実機関係なく)
　　Kuwamai様より
　　　https://github.com/Kuwamai/crane_x7_d435

　・（実機）
　　（多分intelのやつ）

実行する前に、crane_x7_d435/launch/bringup_sim.launch内でincludeされているlaunchファイルの参照先を、team4_robotdesign3_2021に書き換えてください。その後、以下のコマンドを実行してください。gazeboシミュレーションとRvizが立ち上がります。

業務連絡：
　各ディレクトリのREADME.mdは、好きに書き換えてくれて構わない。共有メモの感覚で。
  パス設定方法： (home directory)/.bashrc内最下段に以下を書き込み。あとはいつも道理のビルドをして、(home directory)/.gazebo/models/内の重複ものを消せばOK。
  
  export GAZEBO_MODEL_PATH=$HOME/catkin_ws/src/team4_robotdesign3_2021/description/models:$GAZEBO_MODEL_PATH


中間発表スライド：
https://docs.google.com/presentation/d/1tpdYi2m5gKSQwnyu7kb8FYfR5NCdw_Xt4EQMoiLcIX8/edit#slide=id.p

中間審査スライド：
https://docs.google.com/presentation/d/tpdYi2m5gKSQwnyu7kb8FYfR5NCdw_Xt4EQMoiLcIX8/edit#slide=id.p

最終発表スライド:
https://docs.google.com/presentation/d/1eVwGgFK2r9LaZaNM0u-iIabtcsC3H8CrL7PBDZYyyzY/edit?usp=sharing
