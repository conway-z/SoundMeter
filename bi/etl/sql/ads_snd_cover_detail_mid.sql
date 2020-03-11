
insert into ads_snd_cover_detail_mid
select
    date_format(%s, '%%Y-%%m-%%d') as data_date
    ,date_format(now(), '%%Y-%%m-%%d %%H:%%i:%%S') as nowtime-- 当前年月日
    ,sys1.org_id	-- 组织机构id
    ,sys1.org_simple_name	-- 机构简称
    ,sys1.organization_name -- 机构名称
    ,date_format(sys1.create_time, '%%Y-%%m-%%d %%H:%%i:%%S') as organization_create_time	-- 创建时间(这个字段的原先类型需为datetime，如果是VARCHAR就会报错1292)
    ,la1.name as org_city -- 机构所在市
		,la2.name as org_area -- 机构所在区
		-- ,sys1.org_city	-- 机构所在市
    -- ,sys1.org_area	-- 机构所在区
    -- ,sys1.org_detail	-- 机构详细地址
    ,case when sys2.org_id = 8888 then sys1.org_id	
          else sys2.org_id
    end as zorg_id  -- 总行机构id
    ,case when sys2.org_id = 8888 then sys1.organization_name
          else sys2.organization_name
    end as zorganization_name	-- 总行机构名称
    ,case when sys2.org_id = 8888 then sys1.org_simple_name
          else sys2.org_simple_name
    end as zorganization_name_simple	-- 总行机构简称
    ,t1.supply38-- 供需分发员人数 
    ,t2.supply39-- 供需客户经理人数 
		,case when t1.supply38 > 0 and t2.supply39 > 0 then '是'
					else '否'
					end as is_cover -- '是否覆盖'
    ,case when su.org_id is not null then '是'
          else '否'
    end as is_order -- 管理员是否覆盖
		,date_format(su.create_time, '%%Y-%%m-%%d %%H:%%i:%%S') as order_create_time -- 最早覆盖时间
    ,case when lp.branch_bank_id is not null then '是'
          else '否'
    end as branch_bank_id -- 是否有订单
		,date_format(lp.create_time, '%%Y-%%m-%%d %%H:%%i:%%S')  as branch_create_time  -- 最早订单时间
    
from 
    -- 机构信息
    sys_organization  sys1
   LEFT JOIN 
   -- 关联出总行信息
   sys_organization sys2 
   ON SUBSTRING_INDEX(SUBSTRING_INDEX(sys1.ancestors,',',4),',',-1) = sys2.org_id 
LEFT JOIN
    ( 
-- 确认平台是否有配置管理员
    SELECT su1.org_id,
			min(create_time)as create_time -- 最早时间
        -- ,user_name	-- 用户昵称(0后台1前台)
    FROM sys_user su1
    LEFT JOIN 
    sys_user_role sur1 
    ON su1.user_id = sur1.user_id
    WHERE sur1.role_id IN (33,34,35,54,55) 
    and su1.del_flag = 0
    GROUP BY su1.org_id 
    ) su 
on sys1.org_id = su.org_id

LEFT JOIN
    (
    -- 供需分发员人数统计
    SELECT su1.org_id
        ,count(su1.user_id)as supply38 -- 供需分发员人数 
    FROM 
    sys_user su1
    LEFT JOIN 
    sys_user_role sur1 
    ON su1.user_id = sur1.user_id
    WHERE sur1.role_id = 38 
    and su1.del_flag = 0
    GROUP BY su1.org_id
  ) t1 
on t1.org_id = sys1.org_id
  
LEFT JOIN
    (
    -- 供需客户经理人数统计
    SELECT su1.org_id
        ,count(su1.user_id) as supply39 -- 供需客户经理人数 
    FROM 
    sys_user su1
    LEFT JOIN 
    sys_user_role sur1 
    ON su1.user_id = sur1.user_id
    WHERE sur1.role_id = 39
    and su1.del_flag = 0
    GROUP BY su1.org_id
  ) t2 
  on t2.org_id = sys1.org_id

left join 
    (
		-- 获取所有有订单的银行机构
		select 
    branch_bank_id,
		min(create_time) as create_time-- 最早时间
    from
    loan_product_apply
    where date_format(create_time, '%%Y%%m%%d') < date_format(%s,'%%Y%%m%%d')
		and deleted='0'     
		and enterprise_name != '杭州广鸿贸易有限公司'
    group by branch_bank_id
    )lp
on sys1.org_id = lp.branch_bank_id
left join 
	loan_area la1   -- 回补城市
on sys1.org_city_id = la1.id

left join 
	loan_area la2  -- 回补地区
on sys1.org_area_id = la2.id

where sys1.del_flag = 0
and sys1.org_id not in (6666,8888,9541)
AND sys1.org_type_id between 1008 and 1017