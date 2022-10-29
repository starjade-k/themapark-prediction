CREATE TABLE "LOTTEWORLD_PRC" (
	"LWP_IDX"	int	 GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"AGES"	varchar(30)		NULL,
	"TICKET_GUBUN"	varchar(30)		NULL,
	"PRICE"	int		NULL
);

COMMENT ON COLUMN "LOTTEWORLD_PRC"."AGES" IS '연령대';

COMMENT ON COLUMN "LOTTEWORLD_PRC"."TICKET_GUBUN" IS '이용권구분(1Day / After4)';

COMMENT ON COLUMN "LOTTEWORLD_PRC"."PRICE" IS '이용권가격';

CREATE TABLE "SEOULPARK_PRC" (
	"SPP_IDX"	int	 GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"AGES"	varchar(30)		NULL,
	"TICKET_GUBUN"	varchar(30)		NULL,
	"PRICE"	int		NULL
);

COMMENT ON COLUMN "SEOULPARK_PRC"."AGES" IS '연령대';

COMMENT ON COLUMN "SEOULPARK_PRC"."TICKET_GUBUN" IS '이용권구분';

COMMENT ON COLUMN "SEOULPARK_PRC"."PRICE" IS '이용권가격';

CREATE TABLE "CHILDPARK_PRC" (
	"CPP_IDX"	int	 GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"AGES"	varchar(30)		NULL,
	"TICKET_GUBUN"	varchar(30)		NULL,
	"PRICE"	int		NULL
);

COMMENT ON COLUMN "CHILDPARK_PRC"."AGES" IS '연령대';

COMMENT ON COLUMN "CHILDPARK_PRC"."TICKET_GUBUN" IS '이용권구분';

COMMENT ON COLUMN "CHILDPARK_PRC"."PRICE" IS '이용권가격';

CREATE TABLE "EVERLAND_PRC" (
	"ELP_IDX"	int	 GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"AGES"	varchar(30)		NULL,
	"TICKET_GUBUN"	varchar(30)		NULL,
	"PRICE"	int		NULL
);

COMMENT ON COLUMN "EVERLAND_PRC"."AGES" IS '연령대';

COMMENT ON COLUMN "EVERLAND_PRC"."TICKET_GUBUN" IS '이용권구분';

COMMENT ON COLUMN "EVERLAND_PRC"."PRICE" IS '이용권가격';

CREATE TABLE "SEOULPARK_PARKING" (
	"SP_IDX"	int	 GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"PARKING_NUM"	int		NULL,
	"PARKING_AREA"	int		NULL,
	"PARKING_GUBUN"	varchar(30)		NULL
);

COMMENT ON COLUMN "SEOULPARK_PARKING"."PARKING_NUM" IS '주차면수';

COMMENT ON COLUMN "SEOULPARK_PARKING"."PARKING_AREA" IS '주차장면적(제곱미터)';

COMMENT ON COLUMN "SEOULPARK_PARKING"."PARKING_GUBUN" IS '주차장구분';

CREATE TABLE "CHILDPARK_PARKING" (
	"CP_IDX"	int	 GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"PARKING_NUM"	int		NULL,
	"PARKING_AREA"	int		NULL,
	"PARKING_LOC"	varchar(30)		NULL
);

COMMENT ON COLUMN "CHILDPARK_PARKING"."PARKING_NUM" IS '주차면수';

COMMENT ON COLUMN "CHILDPARK_PARKING"."PARKING_AREA" IS '주차장면적(제곱미터)';

COMMENT ON COLUMN "CHILDPARK_PARKING"."PARKING_LOC" IS '주차장위치';

CREATE TABLE "PRE_ENTRANCE" (
	"PE_IDX"	int	 GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"THEME_NAME"	varchar(30)		NULL,
	"STD_DATE"	date		NULL,
	"ENT_NUM"	int		NULL
);

COMMENT ON COLUMN "PRE_ENTRANCE"."THEME_NAME" IS '테마파크이름';

COMMENT ON COLUMN "PRE_ENTRANCE"."STD_DATE" IS '날짜(일별)';

COMMENT ON COLUMN "PRE_ENTRANCE"."ENT_NUM" IS '입장객수';


CREATE TABLE "THEMEPARK_TIME" (
	"TT_IDX"	int	 GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"THEME_NAME"	varchar(50)		NULL,
	"STD_DATE"	date		NULL,
	"START_TIME"	varchar(10)		NULL,
	"END_TIME"	varchar(10)		NULL
);

COMMENT ON COLUMN "THEMEPARK_TIME"."THEME_NAME" IS '테마파크명';

COMMENT ON COLUMN "THEMEPARK_TIME"."STD_DATE" IS '날짜(일별)';

COMMENT ON COLUMN "THEMEPARK_TIME"."START_TIME" IS '시작시간';

COMMENT ON COLUMN "THEMEPARK_TIME"."END_TIME" IS '종료시간';

CREATE TABLE "THEMEPARK_HOLFAC" (
	"TH_IDX"	int	 GENERATED BY DEFAULT AS IDENTITY	NOT NULL,
	"THEME_NAME"	varchar(50)		NULL,
	"FAC_NAME"	varchar(50)		NULL,
	"STD_DATE"	date		NULL
);

COMMENT ON COLUMN "THEMEPARK_HOLFAC"."THEME_NAME" IS '테마파크명';

COMMENT ON COLUMN "THEMEPARK_HOLFAC"."FAC_NAME" IS '운휴시설명';

COMMENT ON COLUMN "THEMEPARK_HOLFAC"."STD_DATE" IS '날짜(일별)';

ALTER TABLE "LOTTEWORLD_PRC" ADD CONSTRAINT "PK_LOTTEWORLD_PRC" PRIMARY KEY (
	"LWP_IDX"
);

ALTER TABLE "SEOULPARK_PRC" ADD CONSTRAINT "PK_SEOULPARK_PRC" PRIMARY KEY (
	"SPP_IDX"
);

ALTER TABLE "CHILDPARK_PRC" ADD CONSTRAINT "PK_CHILDPARK_PRC" PRIMARY KEY (
	"CPP_IDX"
);

ALTER TABLE "EVERLAND_PRC" ADD CONSTRAINT "PK_EVERLAND_PRC" PRIMARY KEY (
	"ELP_IDX"
);

ALTER TABLE "SEOULPARK_PARKING" ADD CONSTRAINT "PK_SEOULPARK_PARKING" PRIMARY KEY (
	"SP_IDX"
);

ALTER TABLE "CHILDPARK_PARKING" ADD CONSTRAINT "PK_CHILDPARK_PARKING" PRIMARY KEY (
	"CP_IDX"
);

ALTER TABLE "PRE_ENTRANCE" ADD CONSTRAINT "PK_PRE_ENTRANCE" PRIMARY KEY (
	"PE_IDX"
);

ALTER TABLE "THEMEPARK_TIME" ADD CONSTRAINT "PK_THEMEPARK_TIME" PRIMARY KEY (
	"TT_IDX"
);

ALTER TABLE "THEMEPARK_HOLFAC" ADD CONSTRAINT "PK_THEMEPARK_HOLFAC" PRIMARY KEY (
	"TH_IDX"
);

