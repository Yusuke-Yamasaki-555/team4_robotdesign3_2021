# Team4_RobotDesign3_2021
cit robot-design-3-2021 crane_x7
---
## このパッケージについて
- このパッケージは、株式会社アールティ(以下、RT)様([公式サイトはこちら](https://rt-net.jp/))より販売されているcrane_x7を制御するものです。前提として、RT様から配布されている[オリジナルのパッケージ](https://github.com/rt-net/crane_x7_ros)が必要です。

## ライセンス・各種情報について
- crane_x7についての各種情報は、RT様より公開されている[CRANE-X7_Informations](https://github.com/rt-net/crane_x7)よりご参照ください。

- このパッケージは、RT様のライセンスに則っています。詳細は、リポジトリに同梱されている**LICENSE**ファイルをご参照ください。

- このパッケージ内には、RT様から公開されているオリジナルのパッケージを元に作成されたプログラムが含まれています。詳細は、リポジトリに同梱されている**package.xml**ファイルをご参照ください。
---
## 概要
- 　このリポジトリは、crane_x7に居合斬り(?)をさせるROSパッケージです。
- 動作の流れは、以下の画像を参照してください。
![motion process]()

- nodeの構成は、以下の画像を参照してください。
![node]()

- [動作の様子](<youtubeへのリンク>)(リンク先：Youtube)

- なお、動作の一つとして特定のARマーカーを持つ印を見つけた時に嫌がる動作があります。この特定のARマーカーを持つ印を、シュミレータ上では他の印と同様のモデルを使用していますが、動作の様子を映した映像では金色のうんこのモデルを使用しています。
---
## 実行環境
- ROS Noetic
- Ubuntu 20.04.3 LTS
- ROS Distribution: Noetic Ninjemys 1.15.7
- Rviz 
- Gazebo 
- Moveit!ライブラリ

- 以上の基本に加えて、このパッケージが提供する動作は、Intel RealSence Depth Camera D435(以下、D435)([公式サイトはこちら](https://www.intelrealsense.com/depth-camera-d435/))の使用を前提としています。

- 動作を行う環境は、以下の図を参照してください。
---
## パッケージ内容
#### action/
- actionに使用するmessageファイル置き場

#### description/
- シュミレータで使用するモデル置き場

#### launch/
- launchファイル置き場

#### scripts/
- 実行プログラム置き場

#### srdf/
- srdfファイル置き場

#### srv/
- serviceに使用するmessageファイル置き場
---
## セットアップ
- 必ず、事前に実行環境の構築を行った上で、以下を行ってください。
### １．関連パッケージのインストール 
- 以下のどちらかのコマンドを実行して、~/catkin_ws/src/ 上にこのパッケージをインストールしてください。
```bash
$ git clone https://github.com/Yusuke-Yamasaki-555/Team4_RobotDesign3_2021.git # HTTPS通信の場合
$ git clone git@github.com:Yusuke-Yamasaki-555/Team4_RobotDesign3_2021.git # SSH通信の場合
```
- D435のシュミレータへのモデルの適用のため、Kuwamai様より公開されている[パッケージ](https://github.com/Kuwamai/crane_x7_d435)をインストールしてください。
- また、実機で実行する場合、別途RealSenceをROSで利用するためのパッケージをいくつかインストールする必要があります。

- 以上が完了したら、以下のコマンドを使用してビルドしてください。
```bash
$ ~/catkin_ws && catkin_make
$ source ~/catkin_ws/devel/setup.bash
```

### ２．起動
#### シュミレータの場合
- 実行する前に、**~/catkin_ws/src/crane_x7_d435/launch/bringup_sim.launch**内の６行目の、**$(find <パッケージ名>)**のパッケージ名を、**team4_robotdesign3_2021**に書き換えてください。
- 実行する前に、**~/.bashrc**内の一番下に、以下のコードを書き込んでください。
```bash
export GAZEBO_MODEL_PATH=$HOME/catkin_ws/src/team4_robotdesign3_2021/description/models:$GAZEBO_MODEL_PATH
```
- 以上が完了したら、ビルドをしてください。

- 以下のコードを実行することで、シュミレータが起動します。
```bash
$ roslaunch crane_x7_d435 bringup_sim.launch
```

#### 実機の場合
- 実行する前にcrane_x7をPCに接続し、以下のコマンドを実行してデバイスドライバに実行権限を与えます。
```bash
$ sudo chmod 666 /dev/ttyUSB0実行
```
- 以下のコマンドを実行することでRvizとcrane_x7が起動します。
```bash
$ roslaunch realsense2_camera rs_camera.launch
$ roslaunch crane_x7_bringup demo.launch fake_execution:=false
```

### ３．実行
- 以下のコマンドを実行することで、crane_x7が居合斬り(?)をしてくれます。(シュミレータ・実機共通)
```bash
$ roalaunch team4_robotdesign3_2021 test.launch
```

- (実機で実行した場合、まれに動作の途中でcrane_x7の第２関節の動力が失われる事例を確認しています。出来る限りこの症状が発生しないようプログラムを組んでいますが、常に完全な動作が出来る保証をすることは出来ません。)


中間発表スライド：
https://docs.google.com/presentation/d/1tpdYi2m5gKSQwnyu7kb8FYfR5NCdw_Xt4EQMoiLcIX8/edit#slide=id.p

中間審査スライド：
https://docs.google.com/presentation/d/tpdYi2m5gKSQwnyu7kb8FYfR5NCdw_Xt4EQMoiLcIX8/edit#slide=id.p

最終発表スライド:
https://docs.google.com/presentation/d/1eVwGgFK2r9LaZaNM0u-iIabtcsC3H8CrL7PBDZYyyzY/edit?usp=sharing
